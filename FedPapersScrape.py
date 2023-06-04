#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Federalist Papers Scrape

@author: natashaliggett
"""

import requests
from bs4 import BeautifulSoup
import os
import pandas as pd 
from nltk.corpus import stopwords
import nltk


## Scrape Federalist Papers 

os.chdir("../")
os.chdir("FedPapers_Modified1")

url = "http://avalon.law.yale.edu/18th_century/fed"
num_papers = 85

for i in range(num_papers):
    num = i + 1
    if num < 10: 
        url_rest = str(0) + str(num) + ".asp"
        file_name = str(0) + str(num) + ".txt"
    else: 
        url_rest = str(num) + ".asp"
        file_name = str(num) + ".txt"
        
    url_full = url + url_rest
    #print(file_name)
    
    r = requests.get(url_full)
    s = BeautifulSoup(r.text)
    
    ps = s.findAll("p")
    file = open(file_name, "w")
    for p in ps:
      t = p.text
      t = t.replace(" Return to the Text", "")
      t = t.replace("Ã\x95", "")
      t = t.replace("Ã¥","")
      # take out words that appear in all documents 
      t = t.replace("PUBLIUS.","") 
      t = t.replace("To the People of the State of New York:","")
      
      # try removing topic realted words: 
      t = t.replace("Constitution","")
      t = t.replace("constitutions","")
      t = t.replace("President","")
      t = t.replace("Senate","")
      t = t.replace("House of Representatives","")
      t = t.replace("United States","")
      t = t.replace("America","")
      t = t.replace("federal","")
      t = t.replace("Articles of Confederation","")
      t = t.replace("Congress","")
      t = t.replace("legislature","")
      t = t.replace("legislative","")
      t = t.replace("law","")
      t = t.replace("Confederacy","")
      t = t.replace("Confederation","")
      t = t.replace("governments","")
      t = t.replace("government","")
      t = t.replace("Supreme Court","")
      t = t.replace("American","")
      t = t.replace("Bill of Rights","")
      t = t.replace("BILL OF RIGHTS","")
      
      t = re.sub('[0-9]+', '', t) # take numbers out 
      file.write(t + "\n")
         
    
# scrape author for each paper 
author = []
r = requests.get("https://www.congress.gov/resources/display/content/The+Federalist+Papers")
s = BeautifulSoup(r.text)
table = s.find("table", {"class": "confluenceTable"})
rows = table.findAll("tr")
for row in rows[1:]:
    author.append(row.findAll("td")[2].text)

# each author will have all his papers merged
hamilton = ""
madison = ""
jay = ""

#os.chdir("Desktop/DataAnalysis/FedPapers")
docnames = [f for f in os.listdir() if f[-4:]==".txt"]
docnames.sort() # makings sure documents are in order 
docnames    


i = 0
for name in docnames: # reading in documents one by one 
    file = open(name) 
    text = file.read() 
    if author[i] == "Hamilton":
        hamilton = hamilton + text
    if author[i] == "Madison":
        madison = madison + text
    if author[i] == "Jay":
        jay = jay + text 
    i = i + 1

    
# use the trigram function to get 100 words mimicking each author 
    
len(hamilton)
len(madison)
len(jay)

# create function that generate trigrams 
def generate_with_trigrams(text, word=None, num=100): 
    tokens = nltk.tokenize.word_tokenize(text)
    trigrams = nltk.trigrams(tokens)
    condition_pairs = (((w0, w1), w2) for w0, w1, w2 in trigrams)
    cfdist = nltk.ConditionalFreqDist(condition_pairs)
    if word is None:
        prev = draw_word(nltk.FreqDist(tokens))
        word = draw_word(nltk.ConditionalFreqDist(nltk.bigrams(tokens))[prev])
    elif len(word.split()) == 1:
        prev = word
        word = draw_word(nltk.ConditionalFreqDist(nltk.bigrams(tokens))[prev])
    else:
        prev, word = word.split()[:2]
    print(prev, end=' ')
    for i in range(1, num):
        print(word, end=' ')
        prev, word = word, draw_word(cfdist[(prev, word)])
        
generate_with_trigrams(hamilton, "The")
generate_with_trigrams(madison, "The")
generate_with_trigrams(jay, "The")
    

## Extracting the tokens' relative frequencies

# read in the files
N = len(docnames)
all_dictionaries = [] # creating empty list of dictionaries 

docs = [None]*N
for i in range(N):
    with open(docnames[i], 'r') as f:
        docs[i] = f.read()


def to_dict(tup, dictionary): 
    dictionary = dict(tup) 
    return dictionary  

stop_words = set(stopwords.words('english'))

for i in range(N): 
    tokens = nltk.tokenize.word_tokenize(docs[i]) # tokenize 
    #words = [w.lower() for w in tokens] # convert to lower case 
    #filtered_tokens = [w for w in words if not w in stop_words] # removed the stop words 
    table = nltk.FreqDist(tokens) # number of times each token occurs 
    
    dictionary = {} # creating empty dictionary
    # table.items() creates tuple of words and their frequencies
    row = (to_dict(table.items(),dictionary)) # row is a dictionary 
    all_dictionaries.append(row) # append to list of dictionaries

M = pd.DataFrame(all_dictionaries) 

# divide each entry in the data frame by the row sum to get the word frequencies for each federalist paper 
data_freq = M.div(M.sum(axis=1), axis=0)
data_freq.fillna(0, inplace=True)

os.chdir("../")

# write to csv 
data_freq.to_csv("WordFreq_TopicWords.csv")

