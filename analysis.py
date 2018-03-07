#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import subprocess as sub
import operator

def load_csv(file: str):
    df = pd.read_csv(file, encoding='utf8', delimiter='|')
    return df

ignore_words = ["the", "and", "it", "was", "who", "what", "when", "where",
"why", "for", "how", "your", "a", "to", "more", "[nl]"]

def word_counts(data):
    count_dict = {}
    for t in data["text"]:
        words = t.split()
        for word in words:
            word = word.lower()
            if word in ignore_words:
                pass
            else:
                if word in count_dict.keys():
                    count_dict[word] = (count_dict[word] + 1)
                else:
                    count_dict[word] = 1
    sorted_dict = sorted(count_dict.items(), key=operator.itemgetter(1))
    return sorted_dict


if __name__ == "__main__":
    sub.call(["python", "main.py"])
    csv = load_csv('tweet_output.csv')
    print(word_counts(csv))
