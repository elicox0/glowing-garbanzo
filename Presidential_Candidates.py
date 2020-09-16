#!/usr/bin/env python
# coding: utf-8

"""
    File name: Presidential_Candidates.py
    Author: Elijah Cox
    Date created: 4/12/2019
"""

import os

import re
import csv
import string
import gensim
import urllib.parse
import requests
import statistics
from bs4 import BeautifulSoup as bs
from gensim import corpora
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

Corpus_dir = ''
Models_dir = ''

def to_text(pathway):    
  with open(pathway) as infile:        
    return infile.read()

def clean(doc):   
  stop = set(stopwords.words('english'))
  exclude = set(string.punctuation) 
  lemma = WordNetLemmatizer() 
  stop_free = " ".join([i for i in doc.lower().split() if i not in stop])    
  punc_free = ''.join(ch for ch in stop_free if ch not in exclude)    
  normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())    
  return normalized


def create_corpus(site, corpus_folder=Corpus_dir):
  '''Starting with the given site, navigates to external links and harvests text to create a corpus, saved as various .txt files in the corpus folder.'''
  
  os.chdir(corpus_folder)
  webpage = requests.get(site)
  soup = bs(webpage.text, "html.parser")

  # Find all <a> tags in the html 
  tags = soup.find_all('a')

  # Find the links by getting the href= attribute on each tag and append them to a list
  links = [tag.get('href') for tag in tags if tag.get('href') != None and 'http' in tag.get('href')] #Optional condition to filter links
  for i, link in enumerate(links):
    #if i < 10: #Change this condition; it should have to do with the length of the text string
    webpage = requests.get(link)
    soup = bs(webpage.text, "html.parser")
    paragraphs = soup.find_all('p')
    if len(paragraphs) > 2:
      # Write the text from the link to a file with the appropriate name
      with open(f'link_{i}.txt', mode = 'w') as fout:
        #fout.write(soup.get_text())
        fout.write(urllib.parse.urlparse(site).netloc + '\n')    
        for i in paragraphs:        
          fout.write(i.get_text() + '\n')


def topic_model(corpus_loc, n_topics = 10, destination = None,candidate_n=None):
  '''Creates a .csv file with one topic from the corpus per column and saves it to destination.'''
  os.chdir(corpus_loc)
  
  # Create a list of all files in the corpus                                
  filenames = [i for i in os.listdir() if re.search(r"\.txt", i)] 
  doc_complete = [to_text(i) for i in filenames]

  # Remove punctuation and stopwords from the files
  # stop = set(stopwords.words('english'))
  # exclude = set(string.punctuation) 
  # lemma = WordNetLemmatizer()
  doc_clean = [clean(doc).split() for doc in doc_complete]  

  # Set the number of topics                                                
  num_topics = n_topics

  # Convert the list of documents (corpus) into Document Term Matrix using a dictionary
  dictionary = corpora.Dictionary(doc_clean)
  doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

  # Create the object for LDA model using gensim library
  Lda = gensim.models.ldamodel.LdaModel
  ldamodel = Lda(doc_term_matrix, num_topics=num_topics, id2word = dictionary, passes=50)
  output = ldamodel.print_topics(num_topics=num_topics, num_words=8)         

  # Format the data
  columns = [[]]*len(output)
  for i in range(len(output)):
    columns[i] = re.findall(r'\"\w+\"', output[i][1])
    columns[i].insert(0,i+1)
  # for k in columns:
  #   print(k)                                                           
  
  # Export the results to a .csv file
  if destination != None:
    os.chdir(destination)
    with open(f'{candidate_n}.csv', mode= 'w') as csvfile:
      writer = csv.writer(csvfile)
      for item in columns:
        writer.writerow(item)

  return columns


def political_info(sitename, candidate_name, corpus_dir, n_topic):
  '''Given a campaign or other website, creates a corpus and then models the topics in it.'''
  os.chdir(corpus_dir)
  create_corpus(sitename, corpus_dir) 
  issues = topic_model(corpus_dir, n_topics = n_topic, destination = Models_dir,candidate_n=candidate_name)


  return issues











for i in political_info("https://www.donaldjtrump.com/", 'Donald Trump', '/gdrive/My Drive/LING/Final Project/Corpus files - Trump', n_topic=5):
  print(i)





for i in political_info("https://joebiden.com/", 'Joe Biden', '/gdrive/My Drive/LING/Final Project/Biden', n_topic=3):
  print(i)





for i in political_info("https://elizabethwarren.com/", 'Elizabeth Warren', '/gdrive/My Drive/LING/Final Project/Warren', n_topic=4):
  print(i)





for i in political_info("https://www.mikebloomberg.com/", 'Mike Bloomberg', '/gdrive/My Drive/LING/Final Project/Bloomberg', n_topic=3):
  print(i)


# Previous Results:

# Trump:
# [1, '"loading"', '"distancing"', '"vulnerable"', '"protocol"', '"adhere"', '"physical"', '"eg"', '"area"']
# [2, '"coronavirus"', '"president"', '"april"', '"trump"', '"announced"', '"march"', '"new"', '"state"']
# [3, '"tweet"', '"twitter"', '"add"', '"trump"', '"president"', '"america"', '"learn"', '"website"']
# [4, '"afford"', '"phase"', '"httpwhitehousegovopeningamerica"', '"health"', '"mikepence"', '"help"', '"penny"', '"please"']
# [5, '"trump"', '"contribution"', '"president"', '"committee"', '"america"', '"federal"', '"election"', '"j"']
# 
# Biden:
# [1, '"biden"', '"loading"', '"text"', '"joebidencom"', '"candidate"', '"actblue"', '"contribution"', '"message"']
# [2, '"joe"', '"biden"', '"president"', '"time"', '"year"', '"cancer"', '"american"']
# [3, '"site"', '"biden"', '"information"', '"president"', '"use"', '"may"', '"content"', '"service"']
# 
# Warren:
# [1, '"census"', '"u"', '"information"', '"respond"', '"answer"', '"law"', '"bureau"', '"2020"']
# [2, '"closing"', '"temporarily"', '"production"', '"primary"', '"forced"', '"facility"', '"nonessential"', '"due"']
# [3, '"warren"', '"elizabeth"', '"work"', '"crisis"', '"grassroots"', '"candidate"', '"people"', '"need"']
# [4, '"information"', '"site"', '"may"', '"cooky"', '"collect"', '"campaign"', '"u"', '"provide"']
# 
# Bloomberg:
# [1, '"information"', '"may"', '"city"', '"u"', '"school"', '"use"', '"new"', '"bloomberg"']
# [2, '"bloomberg"', '"read"', '"city"', '"new"', '"mayor"', '"philanthropy"', '"public"', '"mike"']
# [3, '"new"', '"bloomberg"', '"city"', '"2013"', '"administration"', '"million"', '"nyc"']






