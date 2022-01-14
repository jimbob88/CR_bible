from turtle import ht
import xml.etree.ElementTree as ET
import os
import bs4
import re

bible_html = './engwebpb_html/' # CHANGE THIS TO CHANGE YOUR HTML BIBLE

tree = ET.parse(os.path.join(bible_html, 'engwebpb-VernacularParms.xml'))
root = tree.getroot()


conversion_table = {scripture.attrib['ubsAbbreviation']: scripture.text for scripture in root.findall('scriptureBook')}
regex = (
    r'('+
    '|'.join(conversion_table.keys())+
    r')([\d]+)\.htm'
)
res = [os.path.join(bible_html, f) for f in os.listdir(bible_html) if re.search(regex, f)]
dataset = {
    conv: {} for conv in conversion_table.values()
}
print(regex)
for htm in res:
    if os.path.split(htm)[1][0:3] == 'PSA':
        next
    else:
        print(htm)
        soup = bs4.BeautifulSoup(open(htm, 'r', encoding='utf-8').read(), "lxml")
        # print(soup.find_all('span', {'class': 'verse'}))
        p_verses = []
        for paragraph in soup.find_all('div', {'class': 'p'}):
            p_verses.append([int(v.get('id')[1:]) for v in paragraph.find_all('span', {'class': 'verse'})])
        dataset[conversion_table[re.search(regex, htm).group(1)]][re.search(regex, htm).group(2)] = p_verses    

print(dataset)
        