#!/usr/bin/env python
# -*- coding: utf-8 -*-


import Question
import sys


class Recording:
    def __init__(self, filePath):
        with open(filePath, "r") as myfile:
            lines = myfile.readlines()
            ql = []
            self.questions = []
            for l in lines:
                if l.startswith("QUESTION"):
                    if len(ql) > 0:
                        self.questions.append(Question.Question(ql))
                        ql = []
                else:
                    ql.append(l)
            if len(ql) > 0:
                self.questions.append(Question.Question(ql))
                ql = []

    def printAll(self):
        for i, q in enumerate(self.questions):
            print 'Question-', i
            q.printAll()


def main(filePath):
    r = Recording(filePath)
    r.printAll()

if __name__ == "__main__":
    main(sys.argv[1])
