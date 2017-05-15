import os
import re

for line in open("episode01.txt", "r"):

    line = line.strip().replace("(continued)", "").replace("(CONTINUED)", "").strip()

    if re.match("^[A-Z][A-Z]+", line) and re.match("^[A-Z][A-Z]+$", re.sub("[^A-Za-z!?:]+", "", line)):
        if not "FADE" in line \
                and not "CUT TO" in line \
                and not "WHITE OUT" in line \
                and not "ACT " in line \
                and not "VOICE" in line \
                and not "INTERCUT" in line \
                and not "CLOSE" in line:
            print(line)
        elif not "PEAKS" in line and not "LYNCH" in line:
            print("--")
