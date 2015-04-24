#!/usr/bin/env python
# Copyright (c) 2015 Dagan Martinez
# Under the MIT license

# import modules - tweetalysis includes Tweepy
print("Setting up...")
from tweetalysis import*
import json
import sys
import time

# Authenticate application and create API object
auth = tweepy.OAuthHandler(open("keys/consumer_key", "r").read(), open("keys/consumer_secret", "r").read())
api = tweepy.API(auth)


# Collect tweets
if sys.version_info[0] == 2:
    query = raw_input("\nQuery>")
    max_number_of_results = int(raw_input("Max Results>"))
else:
    query = input("\nQuery>")
    max_number_of_results = int(input("Max Results>"))
print("")
tweets = get_tweets(api, query, max_results=max_number_of_results)  # get 'max' results

# Converting data
sys.stdout.write("Converting Data...          \r")
tweet_texts = []
json_dump = ""
tweetcount = 0
for tweet in tweets:
    tweet_texts.append(tweet.text)
    json_dump += json.dumps(tweet._json)+"\n"
    tweetcount += 1


# Get word counts
sys.stdout.write("Performing Wordcount...          \r")
wordcount = get_word_counts(get_words(tweet_texts, exclude=STOP_WORDS+TWITTER_WORDS+ALPHABET))


# Export JSON
sys.stdout.write("Exporting Data...          \r")
json_file = open("twitter_dump("+query+").json", "w")
json_file.write(json_dump)
json_file.close()


# Export word count
wc_text = ""
for i in wordcount:
    wc_text += i[1]+":"+str(i[0])+"\n"
wc_file = open("twitter_dump("+query+")_wordcount.txt","w")
wc_file.write(wc_text)
wc_file.close()


# Finish
print("Finished:                    ")
print("# of tweets exported:\t"+str(tweetcount))
print("# of words exported:\t"+str(len(wordcount)))
print("Tweets to wordcount:\t"+str(100*tweetcount/len(wordcount))+"%")