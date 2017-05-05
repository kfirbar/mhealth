#!/usr/bin/env python
# -*- coding: utf-8 -*-


from collections import Counter


class Question:
    def __init__(self, lines):
        self.word_count = 0
        self.words = Counter()
        self.lemmas = Counter()
        self.contentLemmas = Counter()
        self.pos = Counter()
        self.number = Counter()
        self.person = Counter()
        self.tense = Counter()
        self.prefixes = Counter()
        for l in lines:
            print l
            self.word_count = self.word_count + 1
            attrs = l.split('\t')
            lemma = ''
            for a in attrs:
                if a.find(':') > -1:
                    parts = a.split(':')
                    key = parts[0].strip()
                    value = parts[1].strip()
                    if key == 'Lemma':
                        self.lemmas[value] += 1
                        lemma = value
                        #if lemma exists, it means that line is valid so the first token in this line is the word surface form
                        self.words[attrs[0]] += 1
                    if key == 'POS':
                        self.pos[value] += 1
                        if value in ('noun', 'verb', 'adverb', 'adjective', 'participle'):
                            self.contentLemmas[lemma] += 1
                    if key == 'Number':
                        self.number[value] += 1
                    if key == 'Person':
                        self.person[value] += 1
                    if key == 'Tense':
                        self.tense[value] += 1
                    if key == 'Prefixes':
                        if value.find('preposition') > -1:
                            self.prefixes['preposition'] += 1
                        if value.find('conjunction') > -1:
                            self.prefixes['conjunction'] += 1
                        if value.find('relativizer') > -1:
                            self.prefixes['relativizer'] += 1

    def mergeWith(self, other):
        self.lemmas = self.lemmas + other.lemmas
        self.words = self.words + other.words
        self.pos = self.pos + other.pos
        self.contentLemmas = self.contentLemmas + other.contentLemmas
        self.number = self.number + other.number
        self.person = self.person + other.person
        self.tense = self.tense + other.tense
        self.prefixes = self.prefixes + other.prefixes
        self.word_count = self.word_count + other.word_count


    def printAll(self):
        mc = self.contentLemmas.most_common(10)
        print "Most common lemmas: "
        for m in mc:
            print m[0], ':', m[1]

