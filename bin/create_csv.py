#! /usr/bin/env python3

from lxml import etree
import glob, csv

files = glob.glob("sourcemeta/*.xml")
all_parsed = []
for f in files:
    filekey = f.split("/")[1].split("_")[0]
    #print(filekey)
    with open(f, 'r') as xml_file:
        xml = etree.fromstring(xml_file.read())
        title = xml.find(".//{*}title").text
        author = xml.find(".//{*}author")
        if author is not None:
            author = author.text
        else:
            author = ""
        date = xml.find(".//{*}date")
        if date is not None:
            date = date.text
        else:
            date = ""
    all_parsed.append({"filekey":filekey,"title":title,"author":author,"date":date})

with open("metadata.csv", "w") as newcsv:
    fieldnames=["filekey", "author", "title", "date"]
    writer = csv.DictWriter(newcsv, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_parsed)
