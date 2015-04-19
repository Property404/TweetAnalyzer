# Dagan Martinez - 2015
# Copyright (c) 2015 Dagan Martinez
# Under the MIT license

import tweepy
from unicodedata import normalize
import sys
import stop_words

# Lists
punctuation = ["http://t.co/", "\n", "\t", "\r", "`", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=",
               "+", ", ", "<", ".", ">", "?", "/", "{", "[", "}", "]", "|", "\\", ":", ";", "'", '"']
STOP_WORDS = stop_words.get_stop_words('en')
TWITTER_WORDS = ["","amp", "http", "https", "co", "com", "rt", "strl", "hstn", "t", "u", "1", "2", "3", "4", "5", "6",
                 "7", "8", "9"]
ALPHABET = list("abcdefghijklmnopqrstuvwxyz")


# Return list of Tweet objects based on search query. Must take tweepy.API object
def get_tweets(api, q, lang=None, max_results=200, result_type='recent'):
    tweets = []
    for tweet in tweepy.Cursor(api.search, q=q, lang=lang, count=100, result_type=result_type).items(max_results):
        tweets.append(tweet)
        sys.stdout.write(str(len(tweets))+" tweets\r")
    return tweets


# Return a list of words from a list of texts
def get_words(texts, exclude=[]):
    # Clean up punctuation and all that jazz (HaCha!)
    # By converting the word list to a string
    words = texts
    tempstring = ""
    for i in words:
        tempstring += normalize('NFKD', i.lower()).encode('ascii', 'ignore').decode("utf-8")+" "  # Remove non-ASCII characters
    for i in punctuation:
        tempstring = tempstring.replace(i, " ")
    while tempstring != tempstring.replace("  ", " "):
        tempstring = tempstring.replace("  ", " ")

    # Convert back to list
    tempwords = tempstring.split(" ")
    words = []
    for i in tempwords:
        if i.lower() not in exclude:
            words.append(i)
    return words


# Return a list of word counts from a list of words
def get_word_counts(words):
    # Create list of word counts
    wordcountlist = []
    usedwordlist = []
    for word in words:
        if word not in usedwordlist:
            count = 0
            for i in words:
                if i == word:
                    count += 1
            wordcountlist.append([word, count])
            usedwordlist.append(word)

    # Bubble sort wordcountlist
    for passnumber in range(len(wordcountlist)-1, 0, -1):
        for i in range(passnumber):
            if wordcountlist[i][1] > wordcountlist[i+1][1]:
                temp = wordcountlist[i]
                wordcountlist[i] = wordcountlist[i+1]
                wordcountlist[i+1] = temp
    # Return result
    return wordcountlist[::-1]