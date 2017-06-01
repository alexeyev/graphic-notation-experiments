# -*- coding: utf-8 -*-a

import re


def read(texts_file):
    parsed = []

    for line in open(texts_file, "r+"):
        line = line.strip().lower()
        splitted = re.findall(r"[\w'<>\]\[]+|[.,!?;]", line)
        parsed.append(splitted)
    return parsed


txts = read("../parsed_texts.txt")

print(txts[0])


def build_matrix(parsed_texts, depth):
    """
    :param parsed_texts:
    :return: (dict, matrix)
    """

    if depth > 3:
        print("Are you fucking crazy? Depth = ", depth, " is too much, you shouldn't go deeper")

    ngram2id = {}
    prefix = ["*" + str(i) for i in range(depth)]
    postfix = prefix[::-1]
    ngram_counter = 0

    next2id = {}
    word_counter = 0

    for text in parsed_texts:

        new_text = prefix + text + postfix
        print(new_text)

        for i in range(len(new_text) - depth):

            print(new_text[i:i + depth])
            t = tuple(new_text[i:i + depth])

            if not t in ngram2id:
                ngram2id[t] = ngram_counter
                ngram_counter += 1
        print(ngram2id)
        quit()

            # todo


print(build_matrix(txts, 4))
