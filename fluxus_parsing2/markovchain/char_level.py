# -*- coding: utf-8 -*-a

import re
from collections import defaultdict

import numpy as np
import scipy.sparse as sp


def read(texts_file):
    parsed = []

    for line in open(texts_file, "r+"):
        line = line.strip().lower().replace("[s]", "S").replace("[e]", "E").replace("<n>", "N")
        splitted = list(line)
        parsed.append(splitted)
    return parsed

WEIRD_SYMBOLS = "йцукенгшщзхъфывапролдячсмитьбю"


def gen_seed(depth):
    return [WEIRD_SYMBOLS[i] for i in range(depth)]


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

    id2next = {}

    transp_list = defaultdict(lambda: 0, {})

    # строим словари индексов
    for text in parsed_texts:

        new_text = prefix + text + postfix
        # print(new_text)

        for i in range(len(new_text) - depth):

            # смотрим на нграмму
            # print(new_text[i:i + depth])
            t = tuple(new_text[i:i + depth])

            if not t in ngram2id:
                ngram2id[t] = ngram_counter
                ngram_counter += 1

            # смотрим на текущее слово
            w = new_text[i]

            if not w in next2id:
                next2id[w] = word_counter
                id2next[word_counter] = w
                word_counter += 1

            # смотрим на следующее слово
            if i + depth - 1 < len(new_text):
                w = new_text[i + depth]
                if not w in next2id:
                    next2id[w] = word_counter
                    id2next[word_counter] = w
                    word_counter += 1

                transp_list[(ngram2id[t], next2id[w])] += 1

    trans_dict = dict(transp_list)
    trans_mx = sp.dok_matrix((ngram_counter, word_counter))

    for kk in trans_dict:
        trans_mx[kk[0], kk[1]] = trans_dict[kk]

    trans_mx = sp.csr_matrix(trans_mx)

    return trans_mx, ngram2id, id2next


def generate_markov_walk(trans_mx, ngram2id, id2next, depth, teleport=0.0):
    prefix = tuple(gen_seed(depth))
    removable = set(prefix).union(set(["S", "E"]))
    next = None
    steps = 1

    result = []

    while next != 0:

        steps += 1
        row = trans_mx[ngram2id[prefix], :]
        denserow = row.todense().A1
        denserow += teleport
        denserow /= np.sum(denserow)
        next = np.random.choice(denserow.shape[0], size=1, p=denserow)[0]
        prefix = prefix[1:] + (id2next[next],)

        written_word = id2next[next]

        if not written_word in removable:
            result.append(written_word)

    return result


class MarkovianCharLevelGenerator(object):
    def __init__(self, depth=2, teleport=0.0):
        self.depth = depth
        self.teleport = teleport

    def fit(self, texts, start_item, end_item):
        trans_mx, ngram2id, id2next = build_matrix(texts, self.depth)
        self.trans_mx = trans_mx
        self.ngram2id = ngram2id
        self.id2word = id2next
        return self

    def generate_list(self):
        return generate_markov_walk(trans_mx=self.trans_mx,
                                    ngram2id=self.ngram2id,
                                    id2next=self.id2word,
                                    depth=self.depth,
                                    teleport=self.teleport)

    def generate_text(self):
        return "".join([w.replace("N", "\n") for w in self.generate_list()]).replace(" .", ".").replace(" ,", ",")


TEXTS = read("../parsed_texts.txt")

if __name__ == "__main__":
    depths = range(15)
    generators = [MarkovianCharLevelGenerator(depth=d + 1).fit(TEXTS) for d in depths]

    for id, gen in enumerate(generators):
        print()
        print("DEPTH", id + 1)
        print(gen.generate_text())
