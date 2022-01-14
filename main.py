import xml.etree.ElementTree as ET
import os
import glob
import bs4

bible_html = './engwebpb_html/' # CHANGE THIS TO CHANGE YOUR HTML BIBLE

tree = ET.parse(os.path.join(bible_html, 'engwebpb-VernacularParms.xml'))
root = tree.getroot()


conversion_table = [(scripture.attrib['ubsAbbreviation'], scripture.text) for scripture in root.findall('scriptureBook')]

for htm in glob.glob(os.path.join(bible_html, '*.htm')):
    if os.path.split(htm)[1][0:3] == 'PSA':
        next
    else:
        soup = bs4.BeautifulSoup(open(htm, 'r', encoding='utf-8').read(), "lxml")
        print(soup.find_all('span', {'class': 'verse'}))