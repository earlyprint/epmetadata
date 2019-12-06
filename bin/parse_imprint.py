#! /usr/bin/env python3

from lxml import etree
import glob, re
from collections import defaultdict
import pandas as pd
from random import sample

def preprocess(pub_text):
    # print(pub_text)
    pub_text = re.sub('^(?:[EeIij][mn])?[Pp][ir][iye]nt[ye]d and(?: are)?(?: to)?(?: be)? [Ssh]?ou?lde? by ([A-Z](?:\.|[a-z]+\.?) ?)([A-Z](?:\.|[a-z]+\.?)),?', r'printed by '+r'\g<1>'+r'\g<2>'+' and sold by '+r'\g<1>'+r'\g<2>', pub_text)
    pub_text = re.sub('^(?:[EeIij][mn])?[Pp][ir][iye]nt[ye]d and(?: are)?(?: to)?(?: be)? [Ssh]?ou?lde? for ([A-Z](?:\.|[a-z]+\.?) ?)([A-Z](?:\.|[a-z]+\.?)),?', r'printed for '+r'\g<1>'+r'\g<2>'+' and sold by '+r'\g<1>'+r'\g<2>', pub_text)
    pub_text = re.sub(r"\.\.\.","",pub_text)
    pub_text = pub_text.strip(",: ;?")
    return pub_text

def basic_match(pub_text):
    basic_re = r"(?:\[?by|^\[?[Bb]y|\band by) (?P<printer>.*?(?=(?:\bfor\b|\band are\b|\band sold\b|\bat\b|\b(?:with)?in\b|\bby\b|\bd(?:w|vv)ell[iy]nge?\b|\b(?<!the )(?:[Pp]r[iy]nters?|[Ss]er[vu]ants?) (?:[uv]n)?to\b|\bne[ae]re?\b|\bliving\b|\bto be\b|\band reprinted\b|\b(?:the )?assigne?e?s?(?:ment)?\b|\bon\b|\b[Aa]nno\b|\b[Cc]um\b|\bnot farr?e?\b|\b(?:W|VV|vv|w)ith\b|\b[Pp]ermissu\b|$)))|\bfor (?P<publisher>.*?(?=(?:\bfor\b|\band are\b|\band published\b|\band sold\b|\bat\b|\b(?:with)?in\b|\bby\b|\bd(?:w|vv)ell[iy]nge?\b|\bne[ae]re?\b|\bto be\b|\b(?:[Pp]r[iy]nters?|[Ss]er[vu]ants?) (?:[uv]n)?to\b|\band reprinted\b|\b(?:the )?assigne?e?s?(?:ment)?\b|\bon\b|\bbooke?-?seller\b|\b[Aa]nno\b|\b[Cc]um\b|\bnot farr?e?\b|\b(?:W|VV|vv|w)ith\b|\b[Pp]ermissu\b|$)))|\b[Ssh]?ou?ld?e? by (?P<bookseller>.*?(?=(?:\band are\b|\bat\b|\bin\b|\bby\b|\bd(?:w|vv)ell[iy]nge?\b|\bne[ae]re?\b|\bon\b|\bbooke?-?seller\b|\b[Aa]nno\b|\b[Cc]um\b|\bnot farr?e?\b|\b(?:W|VV|vv|w)ith\b|\b[Pp]ermissu\b|$)))|\b(?:at|d(?:w|vv)ell[iy]nge? (?:without|in)|in|ne[ae]re?|over against|next|within|on) (?P<location>.*?(?=(?:\bby\b|\band by\b|\band for\b|\bfor\b|$)))|\b(?:the )?assigne?e?s?(?:ment)? of (?P<assigns>.*?(?=(?:\bfor\b|\band are\b|\band sold\b|\bat\b|\b[Ssh]?ou?ld?e?\b|\b(?:with)?in\b|\bby\b|\bd(?:w|vv)ell[iy]nge?\b|\b(?<!the )(?:[Pp]rinters?|[Ss]er[vu]ants?) (?:[uv]n)?to\b|\bne[ae]re?\b|\bliving\b|\bto be\b|\band reprinted\b|\b(?:the )?assigne?e?s?(?:ment)?\b|\bon\b|$)))|\b(?<!the )(?:[Pp]rinters?|[Ss]er[uv]ants?) (?:[uv]n)?to (?P<patron>.*?(?=(?:\bfor\b|\breprinted\b|\band are\b|\band sold\b|\bat\b|\b(?:with)?in\b|\bby\b|\bd(?:w|vv)ell[iy]nge?\b|\b(?<!the )[Pp]rinters? to\b|\bne[ae]re?\b|\bliving\b|\bto be\b|\band reprinted\b|\b(?:the )?assigne?e?s?(?:ment)?\b|\bon\b|\b\d+|$)))"
    m = re.finditer(basic_re, pub_text)
    new_dict = defaultdict(list)
    for g in m:
        for k,v in g.groupdict().items():
            new_dict[k].append(v)
    all_parsed = {k:clean_list(v) for k,v in new_dict.items()}
    return all_parsed

def clean_list(l):
    return sorted(list(set(list(sum([re.split(r"(?:, \[?and | \[?and | \& |, | \.\.\. |)(?![a-z])", item.strip(', /()')) for item in l if item is not None], [])))))

def add_internal_xml(pub_text, parsed_dict):
    for k,v in parsed_dict.items():
        if v != []:
            for name in v:
                if name != "":
                    if k != "location":
                        pub_text = pub_text.replace(name, "<persName type='{}'>{}</persName>".format(k,name))
                    else:
                        pub_text = pub_text.replace(name, "<placeName>{}</placeName>".format(name))
    pub_text = "<publisher>{}</publisher>".format(pub_text)
    pub_text = pub_text.replace('&', '&amp;')
    new_xml = etree.fromstring(pub_text)
    return new_xml

def add_lists(root,parsed_dict):
    if any(v != [] for k,v in parsed_dict.items() if k != 'location'):
        listPerson = etree.SubElement(root, "listPerson")
        for k,v in parsed_dict.items():
            if k != "location" and v != []:
                for name in v:
                    if name != "":
                        person = etree.SubElement(listPerson, "person")
                        person.set("type", k)
                        persName = etree.SubElement(person, "persName")
                        persName.text = name
    if parsed_dict["location"] != []:
        listPlace = etree.SubElement(root, "listPlace")
        for name in parsed_dict["location"]:
            if name != "":
                place = etree.SubElement(listPlace, "place")
                place.set("type", "location")
                placeName = etree.SubElement(place, "placeName")
                placeName.text = name

if __name__ == "__main__":
    files = glob.glob("sourcemeta/*.xml")
    all_parsed = {}
    for f in files:
        filekey = f.split("/")[1].split("_")[0]
        #print(filekey)
        with open(f, 'r') as xml_file:
            xml = etree.fromstring(xml_file.read())
            pubStmt = xml.find(".//{*}publicationStmt")
            publisher = xml.find(".//{*}publisher")
            if publisher is not None:
                pub_text = publisher.text
                processed_pub_text = preprocess(pub_text)
                parsed_pub_text = basic_match(processed_pub_text)
                # print(parsed_pub_text)
                #print()
                if parsed_pub_text != {}:
                    # print(etree.tostring(pubStmt, pretty_print=True))
                    new_xml = add_internal_xml(pub_text, parsed_pub_text)
                    pubStmt.replace(publisher,new_xml)
                    add_lists(xml, parsed_pub_text)
                    print(etree.tostring(xml, pretty_print=True))
                    # all_parsed[filekey] = parsed_pub_text
                    # all_parsed[filekey]['orig_text'] = pub_text




# df = pd.DataFrame(all_parsed)
# df = df.T

# df.to_csv("~/publisher_parsed_nomissing.csv")
