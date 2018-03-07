#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import API
import simplejson as json
import csv
import os




class Listener(StreamListener):
    def __init__(self, time_limit, tweet_limit=1):
        """ Initializer for Listener Class """
        self.time = time.time.now()
        self.limit = time_limit
        self.tweet_counter = 0
        self.tweet_limit = tweet_limit
        self.data = []
        self.StreamObj = None

    def on_data(self, tweet):
        """ When data comes in, this appends the data and adds to counter """
        if self.tweet_counter <= self.tweet_limit:
            self.data.append(tweet)

            self.tweet_counter += 1
            print("{0} Tweet/s Downloaded".format(self.tweet_counter))
        else:
            self.StreamObj.disconnect()
            results.extend(self.data[:-1])


class tweet():
    def __init__(self, tweetId, createdAt, text, userId, hashtags):
        self.tweetId = tweetId
        self.createdAt = createdAt
        self.text = text
        self.userId = userId
        self.hashtags = hashtags

    def to_record(self):
        return [self.tweetId, self.createdAt, self.text, self.userId, self.hashtags]


def get_tweet_by_id(tweet_ID, api):
    """ Gets a specific tweet by ID """
    tweet = api.get_status(tweet_ID)
    results.extend(tweet._json)


def get_tweets_by_user(screen_name, api, count=100):
    """ Gets most recent up to 200 (maximum allowed by API) tweets by user """
    new_tweets = api.user_timeline(screen_name=screen_name, count=100, tweet_mode='extended')

    for tweet in new_tweets:
        results.append(tweet._json)
    return results


def to_csv(tweet_list: list, file_name='tweet_output.csv', delim='|'):
    try:
        os.remove(file_name)
    except OSError:
        pass

    with open(file_name, "a", encoding='utf8') as file:
        csv_writer = csv.writer(file, delimiter=delim)

        # write headers to file
        csv_writer.writerow(['tweetId', 'text', 'createdAt', 'userId', 'hashtags'])
        for t in tweet_list:
            #print(tweet_value.text.encode('utf8', 'replace'))
            t.text = t.text.replace("\n", " [nl] ")
            csv_writer.writerow([t.tweetId, t.text, t.createdAt, t.userId, t.hashtags])
            # csv_writer.writerow([t.tweetId.encode('utf8', 'replace'), t.text.encode('utf8', 'replace'), t.createdAt.encode('utf8', 'replace'), t.userId.encode('utf8', 'replace')])


def write_json(data: list, file, overwrite: str):
    try:
        os.remove(file)
    except OSError:
        pass

    data = json.dumps(data, ensure_ascii=False, separators=(',', ': '))
    if overwrite is True:
        filemode = 'w'
    else:
        filemode = 'a'
    with open(file, filemode, encoding='utf8') as f:
        f.write(data)


def read_json(file: str):
    with open(file, 'r', encoding='utf8') as f:
        data = json.load(f, encoding='utf8')
    return data

def make_tweet_objects(filename: str):
    tweets = read_json(filename)
    tweets_list = []
    for t in tweets:
        h_list = []
        for hash in t["entities"]["hashtags"]:
            h_list.append(hash["text"])
        t = tweet(t["id_str"], t["created_at"], t["full_text"], t["user"]["id_str"], h_list)
        tweets_list.append(t)
    return tweets_list

def get_tweet_stream(keywords: list, auth, listener: Listener):
    """ Opens connection with API for Stream Listener """
    twitterStream = Stream(auth, listener)
    listener.StreamObj = twitterStream
    twitterStream.filter(track=keywords, languages=['en'])


def setup_auth(
        ckey='L5JVeOVkHIT0lE0hNHHF5ClVr',
        consumer_secret='rS4KyDgoz1MCRIeMVdwOqRD706S0cC5jCvxoYTsINbjWCZLl6f',
        access_token_key='958003558695276544-eUvZUiT2nRfiUWSZjpGGXjYJueh8Khh',
        access_token_secret='7ter6ZZGa9W7Vr3qBqfFwFB36sUQj8g7EQ9KneNJC5IaZ'):
    """ Sets up authentication for Twitter API """
    auth = OAuthHandler(ckey, consumer_secret)  # OAuth object
    auth.set_access_token(access_token_key, access_token_secret)

    api = API(auth)
    return auth, api


def main(keywords: list,
         filename: str,
         byId=False,
         byUser=False,
         byStream=False,
         timeLimit=None,
         tweetLimit=100,
         overwrite=True):
    global results
    results = []

    auth, api = setup_auth()

    if byStream is True:
        listener = Listener(timeLimit, tweetLimit)
        get_tweet_stream(keywords, listener)
    if byId is True:
        for kw in keywords:
            get_tweet_by_id(kw, api)
    if byUser is True:
        for kw in keywords:
            get_tweets_by_user(kw, api, tweetLimit)

    write_json(results, filename, overwrite)
    to_csv(make_tweet_objects('Test_Output.json'))

if __name__ == "__main__":
    main(['Travelers'], 'Test_Output.json', byUser=True)
