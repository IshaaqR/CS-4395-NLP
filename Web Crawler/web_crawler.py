# -*- coding: utf-8 -*-
"""Web Crawler

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lWaUU9reDCsTUAT-ffSEUJLjbAxOko9c
"""

from google.colab import drive
drive.mount('/content/drive')
from bs4 import BeautifulSoup
import requests
import urllib.request
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords

"""Build a web crawler function that starts with a URL representing a topic (a sport, your favorite film, a celebrity, a political issue, etc.) and outputs a list of at
least 15 relevant URLs. The URLs can be pages within the original domain but should have a few outside the original domain. """

def crawl(url):
  r = requests.get(url)
  data = r.text
  soup = BeautifulSoup(data)

  # write urls to a file
  counter = 0
  with open('/content/drive/My Drive/Schoolwork/CS 4395/Web Crawler/urls.txt', 'w') as f:
      for link in soup.find_all('a'):
          # Stop searching if 15 relevant URLs have been found
          if counter >= 15:
            break

          link_str = str(link.get('href'))
          if 'Federer' in link_str or 'federer' in link_str:
              if link_str.startswith('/url?q='):
                  link_str = link_str[7:]
              if '&' in link_str:
                  i = link_str.find('&')
                  link_str = link_str[:i]
              if link_str.startswith('http') and 'google' not in link_str:
                  f.write(link_str + '\n')
                  counter += 1

"""Write a function to loop through your URLs and scrape all text off each page. Store each page’s text in its own file."""

# function to determine if an element is visible
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

def scrape(url, name):
  with open('/content/drive/My Drive/Schoolwork/CS 4395/Web Crawler/raw_text/{}.txt'.format(name), 'w') as f: 
    try:
      html = urllib.request.urlopen(url)
      soup = BeautifulSoup(html)
      data = soup.findAll(text=True)
      result = filter(visible, data)
      temp_list = list(result)      # list from filter
      temp_str = ' '.join(temp_list)

      f.write(temp_str)
    except:
      print('{} could not be scraped'.format(url))

"""Write a function to clean up the textfrom each file. You might need to delete newlines and tabsfirst. Extract sentences with NLTK’s sentence tokenizer. Write the
sentences for each file to a new file. That is, if you have 15 files in, you have 15 files out."""

def process(name):
  with open('/content/drive/My Drive/Schoolwork/CS 4395/Web Crawler/raw_text/{}.txt'.format(name), 'r') as f:
    raw_text = f.read()

  clean_text = " ".join(raw_text.split())

  sents = sent_tokenize(clean_text)
  
  with open('/content/drive/My Drive/Schoolwork/CS 4395/Web Crawler/processed_text/{}.txt'.format(name), 'w') as f:
    for sent in sents:
      f.write(sent)

"""Write a function to extract at least 25 important terms from the pages using an importance measure such as term frequency,or tf-idf. First, it’s a good idea to
lower-case everything, remove stopwords and punctuation. Print the top 25-40 terms."""

def extract():
  full_text = ""
  for i in range(15):
    with open('/content/drive/My Drive/Schoolwork/CS 4395/Web Crawler/processed_text/{}.txt'.format(i), 'r') as f:
      text = f.read().lower()
      full_text += text + " "

  stop_words = stopwords.words('english')
  tokens = word_tokenize(full_text)
  tokens = [w for w in tokens if w.isalpha() and w not in stop_words]
  tokens_set = set(tokens)
  
  # get term frequencies
  tf_dict = {t:tokens.count(t) for t in tokens_set}
  tf_dict = {k: v for k, v in sorted(tf_dict.items(), key=lambda item: -item[1])}
  top_40 = list(tf_dict.keys())[:40]

  return top_40

"""Run the main portion of the code"""

starter_url = "https://en.wikipedia.org/wiki/Roger_Federer"

print("Start of crawler")
crawl(starter_url)
print("End of crawler\n")

print("Start of scraper")
with open('/content/drive/My Drive/Schoolwork/CS 4395/Web Crawler/urls.txt', 'r') as f:
  for i, line in enumerate(f):
    scrape(line, i)
print("End of scraper\n")

print('Started cleaning sentences')
for i in range(15):
  process(i)
print("Finished cleaning sentences\n")

print("Started extracting keywords")
keywords = extract()
print(keywords)
print("Finished extracting keywords\n")

"""Manually determine the top 10 terms from step 4, based on your domain knowledge."""

top_10 = ['federer', 'open', 'grand', 'wimbledon', 'dom', 'tennis', 'return', 'us', 'djokovic', 'nadal']

"""Build a searchable knowledge base of facts that a chatbot (to be developed later) can share related to the 10 terms. The “knowledge base” can be as simple as a Python
 dict which you can pickle. More points for something more sophisticated like sql."""

knowledge_base = {
    'federer': 'Roger Federer is a professional tennis player from Switzerland, and is considered by many to be the best tennis player of our time.',
    'open': 'Most tennis tournaments are called opens (e.g., the Korean Open).',
    'grand': 'Four annual tennis tournaments are called grand slams, and these are the most competitive tournaments to play in.',
    'wimbledon': 'The most famous of the four grand slams, Federer has won this tournament 8 times, the most out of any player ever.',
    'dom': 'Dominic Theim is a younger player with the potential to replace Federer as the world No. 1, having already beat him 5 times out of their 7 games.',
    'us': 'The US Open is another grand slam tournament, with Federer being one of only three players to reach 5 wins in the tournament.',
    'return': 'Federer\'s return is one of his top strengths in tennis, which allows him to return powerful serves from players like Andy Murray.',
    'tennis': 'The tennis world has been dominated by Federer for several years, with few players being able to compete with him.',
    'djokovic': 'Novak Djokovic is one of the few players that can compete with Federer, and is notorious for his two-handed backhand.',
    'nadal': 'Rafael Nadal is Federer\'s lifetime rival, having about the same amount of achievements.'
}
knowledge_base