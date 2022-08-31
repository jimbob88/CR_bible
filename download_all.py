"""
Notice from ebible.org:
------------------------
These sites contain a mixture of copyrighted and Public Domain works. The copyrighted works are individually licensed for use on this site,
each with their own terms agreed to by the copyright owners. Unless they are posted along with a license statement that specifically allows your
intended copying activity, and which you agree to be bound by, you may not copy them without getting permission from the copyright owners. Where
practical, we provide clear licensing and copyright ownership information. However, it is still your own responsibility to verify and comply with
all applicable intellectual property law, including laws pertaining to copyrights and trademarks.
"""
import cgi
import contextlib
import json
import os
import queue
import re
import shutil
import time
import zipfile
from pathlib import Path
from threading import Thread
from typing import Dict, List, Union

import bs4.element

from main import carriage_returns
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0'
}


def bible_list_html(url: str = 'https://ebible.org/download.php', headers=None):
    if headers is None:
        headers = HEADERS

    req = requests.get(url, headers=headers)
    return req.content


def construct_download_link(id_: str):
    return f'https://ebible.org/Scriptures/{id_}_html.zip'


def extract_ids(bible_links: List[bs4.element.Tag], href_regex: str):
    ids = []
    for link in bible_links:
        href = link['href']
        search = re.search(href_regex, href)
        id_ = search[1]
        ids.append(id_)
    return ids


def download_url(url: str, directory):
    """Download file from url to directory

    URL is expected to have a Content-Disposition header telling us what
    filename to use.

    :return: filename of downloaded file.

    Source: Adapted from https://stackoverflow.com/a/34252659
    """
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        raise ValueError('Failed to download')

    filename = url.split('/')[-1]
    print(filename, url)
    abs_path = Path(directory) / filename
    with abs_path.open('wb') as target:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, target)

    return filename


def download(download_queue: queue.Queue, download_list: List[str], artificial_delay: int, directory: Union[Path, str]):
    """Download a list of urls

    :param download_queue: A threading queue to allow things to be downloaded + extracted simultaneously
    :param download_list: The urls to download
    :param artificial_delay: A delay to prevent downloads from being blocked (in seconds)
    """
    for url in download_list:
        filename = Path(directory) / download_url(url, directory)
        print(f'Download Thread: Finished downloading {url} -> {filename}')
        download_queue.put(filename)
        time.sleep(artificial_delay)


def extract(download_queue: "queue.Queue[Path]",
            extract_queue: "queue.Queue[Path]",
            total: int):
    completed = 0
    while completed < total:
        file = download_queue.get()
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(file.parent / file.stem)
        print(f'Extract Thread: Finished extracting {file} -> {file.parent / file.stem}')
        extract_queue.put(file.parent / file.stem)
        completed += 1
        file.unlink(missing_ok=True)


def to_json(extract_queue: "queue.Queue[Path]", total: int, ignore: List[str] = None):
    completed = 0
    while completed < total:
        folder = extract_queue.get()
        folder_name = folder.parts[-1]
        id_ = re.search(r'(.+)_html', folder_name)[1]
        dataset = carriage_returns(folder, f'{id_}-VernacularParms.xml', ignore or [])
        json.dump(dataset, (folder.parent / Path(f'{id_}.json')).open('w', encoding='utf-8'))
        completed += 1
        print(f'JSON Thread: Finished converting {id_} -> {id_}.json')
        folder.unlink(missing_ok=True)


def main():
    content = bible_list_html()
    soup = BeautifulSoup(content, 'lxml')
    href_regex = r'details\.php\?id=(.+)'
    bible_links: List[bs4.element.Tag] = soup.find_all('a', href=re.compile(href_regex))
    ids = extract_ids(bible_links, href_regex)
    html_zips = list(set([construct_download_link(id_) for id_ in ids]))
    download_queue = queue.Queue()
    extract_queue = queue.Queue()

    download_thread = Thread(target=download, args=(download_queue, html_zips, 0.5, Path('./download')))
    extract_thread = Thread(target=extract, args=(download_queue, extract_queue, len(html_zips)))
    json_thread = Thread(target=to_json, args=(extract_queue, len(html_zips)))
    download_thread.start()
    print('Started Download Thread')
    extract_thread.start()
    print('Started Extract Thread')
    json_thread.start()
    print('Started JSON Thread')


if __name__ == '__main__':
    main()
