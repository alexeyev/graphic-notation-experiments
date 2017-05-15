#-*- coding:utf8 -*-
"""
    Code for parsing Fluxus scores obtained via DocViewer
"""
import re

with open("fluxuxs.txt", "r") as flufile:

    skip = 1353

    for line_num, line in enumerate(flufile):
        line = line.strip()
        if len(line) < 3 or line_num < skip:
            continue
        nospace_line = re.sub("\s+", "", line)
        print nospace_line
        quit()
