#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
liwc.py - using LIWC dictionary for sentiment analysis

@author: Yu-Ru Lin
@contact: yuruliny@gmail.com
@date: Jul 22, 2014

'''

import sys,os
import nltk

import time
import string
 
# read in liwc data file
def read_liwc(filename):
    liwc_data = open(filename, "r")
 
    mode = 0
    cat = {}
    dic = {}
 
    for line in liwc_data:
        line = line.strip("\r\n")
	if line.startswith('#'): continue ## replace the line of 'like' with the next line
        if line == "%":
            mode += 1
            continue
 
        elif mode == 1:
            chunks = line.split("\t")
            cat[chunks[0]] = chunks[1]
 
        elif mode == 2:
            chunks = line.split("\t")
            word = chunks.pop(0)
            dic[word] = chunks
 
    return (cat,dic) # cat = list of categories, dic = list of all words with categories
 
# read in dictionary and partition it into set of positive and negative word
def get_wordsets(dic):
    posemo = {}
    negemo = {}
    for word in dic:
        for cat in dic[word]:
            if cat in ['126']:
                posemo[word] = dic[word]
                continue
        for cat in dic[word]:
            if cat in ['19', '127', '128', '129', '130']:
                negemo[word] = dic[word]
                continue
    return (posemo, negemo)
 
# determine if a tweet word matches an LIWC term (including prefix)
def matches(liwc_word, tweet_word):
    if liwc_word[-1] == "*":
        return tweet_word.startswith(liwc_word[:-1])
    else:
        return tweet_word == liwc_word
 
# general purpose function to determine if the string contains any of the
# substrings contained in set
def string_contains_any(string, set):
    for item in set:
        if item in string: return True
    return False

def detect_emoticons(tweet):
    pos_emoticons = [':-)', ':)', '(-:', '(:', 'B-)', ';-)', ';)']
    neg_emoticons = [':-(', ':(', ')-:', '):']
 
    emoticons_flag = 0
    if string_contains_any(tweet, pos_emoticons): emoticons_flag += 1
    if string_contains_any(tweet, neg_emoticons): emoticons_flag -= 1

    return emoticons_flag
    
# returns the positivity/negativity score for the given tweet
def classify(tweet):
    emo = detect_emoticons(tweet)
    if emo!=0: return emo

    # if no emoticons:
 
    tweet = (tweet.lower()).encode('utf-8')
    words = tweet.split(" ")
 
    word_count = 0 #len(words)
    pos_count = 0.0
    neg_count = 0.0
 
    # classify each of the words
    for word in words:
        if len(word) == 0 or word[0] == '@': continue # if the word is prefixed with @, ignore it
        word = word.translate(string.maketrans("",""), string.punctuation) # strip punctuation
 
        # check if the words match posemo/negemo
        for pos in posemo:
            if matches(pos, word):
                pos_count += 1
        for neg in negemo:
            if matches(neg, word):
                neg_count += 1
	word_count += 1
	
    pos_score = pos_count/word_count
    neg_score = neg_count/word_count
 
    if pos_score > neg_score: return 1
    if pos_score < neg_score: return -1
    return 0

def get_text2cat(cat,dic,text):
    cat2cnt = {}
    words = (text.lower()).encode('utf-8')
    words = words.translate(string.maketrans("",""), string.punctuation) # strip punctuation
    words = words.split()
    word_count = len(words)
    cat2cnt.setdefault('wc', word_count)
    dic_count = 0
 
    for word in words:
	for lexicon in dic:
	    if matches(lexicon, word):
		dic_count += 1
		for cid in dic[lexicon]:
		    c = cat[cid]
		    cat2cnt.setdefault(c,0)
		    cat2cnt[c] += 1
    cat2cnt.setdefault('dic_wc', dic_count)
    return cat2cnt
# --- CALLED ON IMPORT --- 
cat, dic = read_liwc('liwc_data/LIWC2007_English131104.dic')

if __name__ == '__main__':
    #posemo, negemo = get_wordsets(dic)
    print get_text2cat(cat,dic,'I am not worried, indeed!')
