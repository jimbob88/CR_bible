from turtle import ht
import xml.etree.ElementTree as ET
import os
import bs4
import re
import json

bible_html = "./engwebpb_html/"  # CHANGE THIS TO CHANGE YOUR HTML BIBLE

tree = ET.parse(os.path.join(bible_html, "engwebpb-VernacularParms.xml"))
root = tree.getroot()

conversion_table = {
    scripture.attrib["ubsAbbreviation"]: scripture.text
    for scripture in root.findall("scriptureBook")
}
ignore = ["PSA", "GLO", "FRT"]
regex = (
    r"("
    + "|".join([key for key in conversion_table.keys() if key not in ignore])
    + r")([\d]+)\.htm"
)
res = [
    os.path.join(bible_html, f) for f in os.listdir(bible_html) if re.search(regex, f)
]
dataset = {conv: {} for ubs, conv in conversion_table.items() if ubs not in ignore}
for htm in res:
    print(htm)
    soup = bs4.BeautifulSoup(open(htm, "r", encoding="utf-8").read(), "lxml")

    p_verses = []
    for paragraph in soup.find_all("div", {"class": "p"}):
        verse_numbers = [
            int(v.get("id")[1:]) for v in paragraph.find_all("span", {"class": "verse"})
        ]
        if len(verse_numbers) > 1:
            p_verses.append(verse_numbers)

    if len(p_verses) > 1:
        dataset[conversion_table[re.search(regex, htm).group(1)]][
            re.search(regex, htm).group(2)
        ] = p_verses

print(dataset)
json.dump(dataset, open("dataset.json", "w", encoding="utf-8"))
