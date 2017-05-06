#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from os import listdir
from os.path import isfile, join
import Recording
import Question
from Embeddings import Embeddings
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from bidi import algorithm as bidialg
import numpy as np
import pandas as pd


def counter2str(c):
    str = ""
    for (k,v) in c.items():
        for i in xrange(v):
            str = str + k + " "
    return str

def counter2normDictionary(c, normVal):
    d = {}
    for (k, v) in c.items():
        d[k] = float(v) / float(normVal)
    return d

def counter2hist(c, title, outputFolder):
    labels, values = zip(*sorted(c.items()))
    indexes = np.arange(len(labels))
    plt.figure(2)
    plt.bar(indexes, values, 1)
    plt.xticks(indexes + 1 * 0.5, labels)
    plt.title(title)
    plt.xticks(indexes, labels, rotation='vertical')
    plt.margins(0.2)
    plt.subplots_adjust(bottom=0.15)
    fig1 = plt.gcf()
    plt.show()
    plt.draw()
    fig1.savefig(join(outputFolder, title), dpi=100)


def buildWordCloud(c, heb, title, outputFolder):
    str = counter2str(c)
    if heb == True:
        str = str.decode("utf-8")
        str = bidialg.get_display(str)

    wordcloud = WordCloud(background_color="white", collocations=False,
                          font_path="/Users/kfirbar/Library/Fonts/Arial.ttf").generate(str)
    plt.axis("off")
    plt.title(title)
    fig1 = plt.gcf()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.draw()
    fig1.savefig(join(outputFolder, title), dpi=100)


def calculate_sentiment_score(c, sentiment_df, embeddings):
    sentiment_score = 0.0
    for (k, v) in c.items():
        k_vec = embeddings.get(k)
        k_sentiment_score = 0.0
        if k_vec is not None:
            k_sentiment_score = sentiment_df["vector"].apply(lambda x: embeddings.similarity(x, k_vec)).mean()
        sentiment_score = sentiment_score + (v * k_sentiment_score)
    return sentiment_score / float(sum(c.values()))

def main(morphFileFolder, outputFolder, embeddings_file, positive_words, negatve_words):
    print "loading embedding vectors..."
    e = Embeddings(embeddings_file)
    print "done!"
    positive_df = pd.read_csv(positive_words)
    negative_df = pd.read_csv(negatve_words)
    positive_df["vector"] = positive_df["word"].apply(lambda x: e.get(x))
    negative_df["vector"] = negative_df["word"].apply(lambda x: e.get(x))

    files = [f for f in listdir(morphFileFolder) if isfile(join(morphFileFolder, f))]
    recordings = []
    for f in files:
        recordings.append(Recording.Recording(join(morphFileFolder, f)))

    questionSummaries = []
    for r in recordings:
        for i in xrange(len(r.questions)):
            if len(questionSummaries) < (i + 1):
                questionSummaries.append(Question.Question([]))

            questionSummaries[i].mergeWith(r.questions[i])

    #specific metrics comparison across all questions
    nouns = {}
    verbs = {}
    adjectives = {}
    adverbs = {}
    content = {}
    person_1 = {}
    person_2 = {}
    person_3 = {}

    for i, q in enumerate(questionSummaries):
        norm_pos = counter2normDictionary(q.pos, q.word_count)
        norm_per = counter2normDictionary(q.person, q.word_count)
        nouns[i + 1] = norm_pos["noun"]
        verbs[i + 1] = norm_pos["verb"]
        adjectives[i + 1] = norm_pos["adjective"]
        adverbs[i + 1] = norm_pos["adverb"]
        content[i + 1] = norm_pos["noun"] + norm_pos["verb"] + norm_pos["adjective"] + norm_pos["adverb"]
        person_1[i + 1] = norm_per["1"]
        person_2[i + 1] = norm_per["2"]
        person_3[i + 1] = norm_per["3"]
        print "Question " + `(i + 1)` + ", avg word count: " + `(q.word_count / len(questionSummaries))`

    counter2hist(nouns, 'Nouns', outputFolder)
    counter2hist(verbs, 'Verbs', outputFolder)
    counter2hist(adjectives, 'Adjectives', outputFolder)
    counter2hist(adverbs, 'Adverbs', outputFolder)
    counter2hist(content, 'Content words', outputFolder)
    counter2hist(person_1, '1st person', outputFolder)
    counter2hist(person_2, '2nd person', outputFolder)
    counter2hist(person_3, '3rd person', outputFolder)


    #raw metrics for each question
    sentiment_scores = {}
    for i, q in enumerate(questionSummaries):

        positive_score = calculate_sentiment_score(q.words, positive_df, e)
        negative_score = calculate_sentiment_score(q.words, negative_df, e)

        print "Question " + `(i + 1)` + ", Positive: " + `positive_score` + ", Negative: " + `negative_score` + ", Overall: " + `(positive_score/negative_score)`
        sentiment_scores[i + 1] = (positive_score/negative_score)
        buildWordCloud(q.contentWords, True, 'Question ' + `(i + 1)` + ' Content Word Cloud', outputFolder)
        counter2hist(counter2normDictionary(q.pos, q.word_count), 'Question ' + `(i + 1)` + ' POS', outputFolder)
        counter2hist(counter2normDictionary(q.person, q.word_count), 'Question ' + `(i + 1)` + ' Person', outputFolder)

    counter2hist(sentiment_scores, 'Sentiment scores', outputFolder)
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])