# coding: utf-8

import os
import re
from bs4 import BeautifulSoup
import json

dir = "fluxusworkbook__1_"

fluxus_texts = []

for f in os.listdir(dir):
    m = re.match("\d+\.html", f)
    if m:
        print(f)
        bs = BeautifulSoup(open(dir + "/" + f, "r+"))
        extrated_text = bs.getText()
        extrated_text = re.sub(r"(\s*\n\s*)+", "NEWLINE", extrated_text)
        extrated_text = re.sub("(NEWLINE)+", "NEWLINE", extrated_text, flags=re.MULTILINE)
        extrated_text = re.sub(r"(\(\d+\)|-\d\d\d\d)", "", extrated_text, flags=re.MULTILINE)
        extrated_text = re.sub(r"D\n*A\ns*T\n*E?\s*U\n*N\n*K\n*N\n*O\n*W\n*N", "DATE UNKNOWN", extrated_text,
                               flags=re.MULTILINE)
        extrated_text = re.sub("(\d\d\d\d|DATE UNKNOWN|UNKNOWN DATE)", r"\1NEWLINE", extrated_text)
        # extrated_text = re.sub("(\d\d\d\d|DATE UNKNOWN)", "\1#NEWLINE#", extrated_text)
        removed_js = re.sub("\S+\s?\{[^\}]+\}", "", extrated_text)
        removed_js = re.sub("NEWLINE", "\n", removed_js)
        removed_js = re.sub(r"\ncontinued\n", "\n", removed_js, re.MULTILINE)
        removed_colontitles = re.sub(
            "(Fluxus Performance Workboo|k, ed. Ken Friedman, Owen Smith & Lauren Sawchyn, Performance Research e-Publications.*|Ken\sFriedman.*)",
            "", removed_js)
        removed_colontitles = re.sub(r"f\nl\nu\nx\nw\no\nr\nk\nb\no\no\nk", "", removed_colontitles, flags=re.MULTILINE)
        removed_colontitles = re.sub(r"\n\d{1,2}\n", "\n", removed_colontitles, flags=re.MULTILINE)
        removed_colontitles = re.sub(r"\n+", "\n", removed_colontitles, flags=re.MULTILINE)
        removed_colontitles = re.sub(r"([A-Z][ \n]){2,20}", "\n", removed_colontitles, flags=re.MULTILINE)
        removed_colontitles = re.sub(r"(\d\d\d\d|DATE UNKNOWN|UNKNOWN DATE)", r"\1DELIMITER", removed_colontitles,
                                     flags=re.MULTILINE)

        splitted = re.split("DELIMITER", removed_colontitles, flags=re.MULTILINE)
        splitted = [" [S] " + s + " [E] " for s in splitted if s.strip()]

        fluxus_texts.extend(splitted)

print("Texts collected: " + str(len(fluxus_texts)))
print("Chars total: " + str(sum([len(t) for t in fluxus_texts])))

wrfile = open("parsed_texts.json", "w+")
json.dump(fluxus_texts, wrfile, ensure_ascii=False)
wrfile.close()

wrfile = open("parsed_texts.txt", "w+")
for line in fluxus_texts:
    wrfile.write(re.sub(r"\n+", " <n> ", line.strip()) + "\n")
wrfile.close()
