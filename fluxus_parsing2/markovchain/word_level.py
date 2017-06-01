# -*- coding: utf-8 -*-a

import re
import scipy.sparse as sp
from collections import defaultdict

import numpy as np


def read(texts_file):
    parsed = []

    for line in open(texts_file, "r+"):
        line = line.strip().lower()
        splitted = re.findall(r"[\w'<>\]\[]+|[.,!?;]", line)
        parsed.append(splitted)
    return parsed


txts = read("../parsed_texts.txt")

print(txts[0])


def gen_seed(depth):
    return ["*" + str(i) for i in range(depth)]


def build_matrix(parsed_texts, depth):
    """
    :param parsed_texts:
    :return: (dict, matrix)
    """

    if depth > 3:
        print("Are you _______ crazy? Depth = ", depth, " is too much, you shouldn't go deeper")

    ngram2id = {}
    prefix = gen_seed(depth)
    postfix = prefix[::-1]
    ngram_counter = 0

    next2id = {}
    word_counter = 0

    transp_list = defaultdict(lambda: 0, {})

    # строим словари индексов
    for text in parsed_texts:

        new_text = prefix + text + postfix
        print(new_text)

        for i in range(len(new_text) - depth):

            # смотрим на нграмму
            # print(new_text[i:i + depth])
            t = tuple(new_text[i:i + depth])

            if not t in ngram2id:
                ngram2id[t] = ngram_counter
                ngram_counter += 1

            # смотрим на следующее слово
            if i + depth - 1 < len(new_text):
                w = new_text[i + depth - 1]
                if not w in next2id:
                    next2id[w] = word_counter
                    word_counter += 1

                transp_list[(ngram2id[t], next2id[w])] += 1

            # смотрим на текущее слово
            w = new_text[i]

            if not w in next2id:
                next2id[w] = word_counter
                word_counter += 1

                # print(ngram2id)
                # print(next2id)
                # print(dict(transp_list))
                # print()
                # quit()
    trans_dict = dict(transp_list)
    trans_mx = sp.dok_matrix((ngram_counter, word_counter))

    for kk in trans_dict:
        trans_mx[kk[0], kk[1]] = trans_dict[kk]

    trans_mx = sp.csr_matrix(trans_mx)

    return trans_mx, ngram2id, next2id


def generate_markov_walk(trans_mx, ngram2id, next2id, depth):
    prefix = tuple(gen_seed(depth))

    print(prefix)
    print("ngram id", ngram2id[prefix])
    row = trans_mx[ngram2id[prefix],]

    print("row ", row)
    print(row.count_nonzero())
    print(row.nonzero())
    print(row.shape)
    # todoL
    # TypeError: sparse matrix length is ambiguous; use getnnz() or shape[0]
    print(np.random.choice(row.shape[1], size=1, p=row[0, :]))



trans_mx, ngram2id, next2id = build_matrix(txts, 2)

print(ngram2id, next2id)

print(generate_markov_walk(trans_mx, ngram2id, next2id, 2))
