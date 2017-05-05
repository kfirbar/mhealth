#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import numpy as np
from numpy import dot
from numpy.linalg import norm
import heapq

class Embeddings:

    def __init__(self, filePath):
        self.embeddings = {}
        with open(filePath, "r") as myfile:
            myfile.readline()   #header
            for line in myfile:
                toks = line.split()
                for i, t in enumerate(toks):
                    if i == 0:
                        self.embeddings[toks[0]] = []
                    else:
                        self.embeddings[toks[0]].append(float(t))
                a = np.array(self.embeddings[toks[0]])
                norm = np.linalg.norm(a, ord=1)
                self.embeddings[toks[0]] = a/norm
        print 'done loading vectors'

    def most_similar(self, word, n):
        res = []
        word_v = self.embeddings[word]
        if word_v is None:
            return []
        for t in self.embeddings:
            res.append([t, dot(word_v, self.embeddings[t])])
        return heapq.nlargest(n, res, key=lambda x: x[1])

    def similarity(self, vec1, vec2):
        if vec1 is None or vec2 is None:
            return 0.0
        return dot(vec1, vec2)

    def word_similarity(self, word1, word2):
        vec1 = self.embeddings.get(word1)
        vec2 = self.embeddings.get(word2)
        if vec1 is None or vec2 is None:
            return 0;
        return self.similarity(vec1, vec2)

    def get(self, word):
        return self.embeddings.get(word)

def main(filePath):
    e = Embeddings(filePath)
    str = 'התלהבות'
    #str = str.decode("utf-8")
    ms = e.most_similar(str, 200)
    for m in ms:
        print m[0]

if __name__ == "__main__":
    main(sys.argv[1])


