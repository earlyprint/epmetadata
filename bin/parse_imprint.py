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
    pub_text = re.sub(r"((\bfor\b|\bsold\sby\b).*and\s)(?:\bby\s)?([A-Z]\.?[a-z]*\.?\s[A-Z]\.?[a-z]*)", r"\g<1>\g<2> \g<3>", pub_text)
    #pub_text = re.sub(r"\.\.\.","",pub_text)
    pub_text = pub_text.strip(",: ;?")
    return pub_text

def basic_match(pub_text):
    """
    This function looks in a cleaned imprint string for text in any of
    five categories: printer, publisher, bookseller, location, assigns,
    and patron. It uses a long regular expression to sort through the
    string and categorize chunks correctly. Then it splits and cleans
    the resulting text using clean_list().
    """

    # A regular expression for the lookahead, which determines when to stop
    # greedily capturing text. This is inserting into the main regex via
    # string formatting.
    ahead = r"(?=(?:\b(?:and\s)?for\b|\band\sare\b|\band\ssold\b|\b\[?sold\b|\bare\b|\bat\b|\b(?:with)?in\b|\bby\b|\bd(?:w|vv)ell[iy]nge?\b|\b(?<!the\s)(?:[Pp]r[iy]nters?|[Ss]er[vu]ants?)\s(?:[uv]n)?to\b|\bne[ae]re?\b|\bliving\b|\bto be\b|\b(?:and\s)?reprinted\b|\b(?:the\s)?assigne?e?s?(?:ment)?\b|\bon\b|\b[Aa]nno\b|\b[Cc]um\b|\bnot\sfarr?e?\b|\b(?:W|VV|vv|w)ith\b|\b[Pp]ermissu\b|\bnigh\b|\b[uv]nto\b|$))"

    # The main regex, which defines the correct categories and
    # assigns them to named capture groups. Verbose mode is
    # turned on to make this more readable.
    basic_re = r"""

(?:\b[Bb]y\b|\b[Aa]nd\s[Bb]y\b|\b[Ii]mprentit\sb[ey]\b)(?P<printer>.*?{ahead})| # Regex for printers, with lookahead

(?:\bfor\b|\bat\sthe\sexpensis\sof\b)(?P<publisher>.*?{ahead})| # Regex for publishers, with lookahead

\b[Ssh]?[oa]u?ld?e?\s\[?by\b(?P<bookseller>.*?{ahead})| # Regex for booksellers, with lookahead

\b(?:[aA]t(?!\slarge)|d(?:w|vv)ell[iy]nge?\s(?:without|in|[uv]pon)|in|[uv]nto|ne[ae]re?|over\sagainst|next|within|on)\b(?P<location>.*?(?=(?:\bby\b|\band\b|\bfor\b|\breprinted\b|$)))| # Regex for location, with custom lookahead to capture as much location as possible in a single string

\b(?:the\s)?assigne?e?s?(?:ment)?\sof\b(?P<assigns>.*?{ahead})| # Regex for assigns, with lookahead

\b(?<!the\s)(?:[Pp]rinters?|[Ss]er[uv]ants?)\s(?:[uv]n)?to\b(?P<patron>.*?{ahead}) # Regex for patron, with lookahead
""".format(ahead=ahead)
    m = re.finditer(basic_re, pub_text, flags=re.VERBOSE)
    new_dict = defaultdict(list)
    for g in m:
        for k,v in g.groupdict().items():
            new_dict[k].append(v)
    all_parsed = {k:clean_list(v) for k,v in new_dict.items()}
    return all_parsed

def clean_list(l):
    cleaned_list = sorted(list(set(list(sum([re.split(r"(?:, \[?and | \[?and | \& |, | \.\.\. |)(?![a-z])", item.strip(', /()')) for item in l if item is not None], [])))))
    cleaned_list = [re.sub(r"\s?\.\.\.\s?", "", c) for c in cleaned_list]
    return cleaned_list

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
