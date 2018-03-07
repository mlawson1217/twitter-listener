#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import subprocess as sub
import operator
import ast

def load_csv(file: str):
    """ Load in csv as dataframe """
    df = pd.read_csv(file, encoding='utf8', delimiter='|')
    return df

ignore_words = ["the", "and", "it", "was", "who", "what", "when", "where",
"why", "for", "how", "your", "a", "to", "more", "[nl]", "of", "from", "with",
"in", "you", "help", "are", "can", "is", "on", "this", "at", "these", "be",
"make", "by", "our", "get", "if", "some", "see", "have", "do", "we", "new", "-", "--", "&amp;"]

def word_counts(data, field):
    """ Counts word frequency in total tweets """
    count_dict = {}
    for t in data[field]:
        words = split_field(t, field)
        for word in words:
            word = clean_word(word)
            if word in ignore_words:
                pass
            else:
                if word in count_dict.keys():
                    count_dict[word] = (count_dict[word] + 1)
                else:
                    count_dict[word] = 1
    sorted_dict = sorted(count_dict.items(), key=operator.itemgetter(1))
    return sorted_dict

def split_field(t, field):
    """ Decides how to handle text vs hashtag field splitting """
    if field is "text":
        words = t.split()
    else:
        words = ast.literal_eval(t)
    return words

def clean_word(word):
    """ Cleans words by lowercasing and replacing """
    word = word.lower()
    word = word.replace(":", "")
    return word

if __name__ == "__main__":
    sub.call(["python", "main.py"])
    csv = load_csv('tweet_output.csv')
    print(word_counts(csv, "text"))
