import xml.etree.ElementTree as ET
import os

bible_html = './engwebp_html/' # CHANGE THIS TO CHANGE YOUR HTML BIBLE

tree = ET.parse(os.path.join(bible_html, 'engwebpb-VernacularParms.xml'))
root = tree.getroot()


