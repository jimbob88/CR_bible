import argparse
import json
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from typing import List, Dict

import bs4


def get_args():
    parser = argparse.ArgumentParser(
        description="A software for getting verse positions by paragraph")
    parser.add_argument('--folder',
                        '-f',
                        required=True,
                        help="choose the folder with the bible dataset")
    parser.add_argument(
        '--xmlname',
        '-x',
        required=True,
        help="select the name of the xml file 'vernacularParms'")
    parser.add_argument('--out',
                        '-o',
                        default='dataset.json',
                        help="the name of the output json")
    parser.add_argument('-i',
                        '--ignore',
                        nargs='+',
                        help='Ignore list',
                        default=['PSA', 'GLO', 'FRT'])

    return parser.parse_args()


def abbreviations(vernacular_parms_xml: Path) -> Dict[str, str]:
    """Given a vernacular parms xml, it discovers all the abbreviations used

    :rtype: dict[str, str]
    :return i.e. {'PSA': 'Psalms'}
    """
    tree = ET.parse(vernacular_parms_xml)
    root = tree.getroot()
    return {
        scripture.attrib["ubsAbbreviation"]: scripture.text
        for scripture in root.findall("scriptureBook")
    }


def htm_filename_regex(abbreviations: List[str], ignore: List[str]):
    """Returns a list of htm file names
    
    :argument abbreviations: i.e. ['PSA', 'GLO', 'FRT']
    :return: A regex, group 1 is the abbreviation, group 2 is the chapter number
    """

    return (r"(" +
            "|".join([key for key in abbreviations if key not in ignore]) +
            r")([\d]+)\.htm")


def filter_folder(folder: Path, regex: str) -> List[Path]:
    """Given a regex, return all file names which match said regex"""
    return [
        element for element in folder.iterdir()
        if element.is_file() and re.search(regex, element.name)
    ]


def paragraphs(soup: bs4.BeautifulSoup) -> List[bs4.Tag]:
    return soup.find_all("div", {"class": "p"})


def verses(element: bs4.Tag):
    return element.find_all("span", {"class": "verse"})


def remove_empty(lst: List):
    return [item for item in lst if item]


def verse_numbers(paragraph: bs4.Tag):
    return [int(verse.get("id")[1:]) for verse in verses(paragraph)]


def paragraph_carriage_returns(soup: bs4.BeautifulSoup):
    """Returns carriage returns that appear on each verse"""
    paragraph_verses = [[
        int(verse.get("id")[1:]) for verse in verses(paragraph)
    ] for paragraph in paragraphs(soup)]
    return remove_empty(paragraph_verses)


def main():
    args = get_args()
    folder = Path(args.folder)

    conversion_table = abbreviations(folder / args.xmlname)
    filename_regex = htm_filename_regex(list(conversion_table.keys()), args.ignore)

    dataset = defaultdict(dict)
    for file in filter_folder(folder, filename_regex):
        book_abbreviation = re.search(filename_regex, file.name).group(1)
        book_name = conversion_table[book_abbreviation]
        chapter = re.search(filename_regex, file.name).group(2)

        soup = bs4.BeautifulSoup(file.read_text('utf-8'), 'lxml')
        p_verses = paragraph_carriage_returns(soup)
        if p_verses:
            dataset[book_name][chapter] = p_verses

    print(dataset)

    json.dump(dataset, Path(args.out).open('w', encoding='utf-8'))


if __name__ == '__main__':
    main()
