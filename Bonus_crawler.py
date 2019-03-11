from __future__ import print_function
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn import svm
from sklearn.svm import SVC
import pandas as pd
from pandas import ExcelWriter
import numpy as np
import platform
from bs4 import BeautifulSoup
import requests
import json
import re

biographyLink = 'https://www.imdb.com/search/title?genres=biography&start=1&ref_=adv_nxt'
actionLink = 'https://www.imdb.com/search/title?genres=action&start=1&ref_=adv_nxt'
comedyLink = 'https://www.imdb.com/search/title?genres=comedy&start=1&ref_=adv_nxt'
linkList = [biographyLink, actionLink, comedyLink]
genresList = ['biography', 'action', 'comedy']
if platform.system() == 'Darwin':
    movieJSONFileList = ['./movies_biography.json',
                         './movies_action.json', './movies_comedy.json']
elif platform.system() == 'Windows':
    movieJSONFileList = ['movies_biography.json',
                         'movies_action.json', 'movies_comedy.json']
moviesLinkSet = set()
for index, link in enumerate(linkList):
    newLink = link
    genreIndex = index
    html = requests.get(link)
    bs = BeautifulSoup(html.text, 'lxml')
    movieListDivs = bs.find_all('div', {'class': 'lister-item mode-advanced'})
    movieList = []
    print('1')
    for index, movieLink in enumerate(movieListDivs):
        if movieLink.find('a')['href'] not in moviesLinkSet:
            print('crawling %d movie of %s' %
                  (index+1, genresList[genreIndex]))
            moviesLinkSet.add(movieLink.find('a')['href'])
            link = 'https://www.imdb.com' + \
                movieLink.find('a')['href'] + '/'
            html = BeautifulSoup(requests.get(link).text, 'lxml')
            name = html.find('h1').text
            storyLine = html.find('div', {'id': 'titleStoryLine'}).find(
                'div', {'class': 'inline canwrap'}).find('span').text
            movie = {"name": name, "storyline": storyLine,
                     "genre": genresList[genreIndex], "link": link}
            movieList.append(movie)
    while (len(moviesLinkSet) % 50) != 0:
        pageNumber = re.findall(r'\d', newLink)
        newLink = re.sub(r'\d', str(int(pageNumber[0])+50), newLink)
        html = requests.get(newLink)
        bs = BeautifulSoup(html.text, 'lxml')
        movieListDivs = bs.find_all(
            'div', {'class': 'lister-item mode-advanced'})
        for index, movieLink in enumerate(movieListDivs):
            print('crawling %d extra movie of %s' %
                  (index+1, genresList[genreIndex]))
            if movieLink.find('a')['href'] not in moviesLinkSet:
                moviesLinkSet.add(movieLink.find('a')['href'])
                link = 'https://www.imdb.com' + \
                    movieLink.find('a')['href'] + '/'
                html = BeautifulSoup(requests.get(link).text, 'lxml')
                name = html.find('h1').text
                storyLine = html.find('div', {'id': 'titleStoryLine'}).find(
                    'div', {'class': 'inline canwrap'}).find('span').text
                movie = {"name": name, "storyline": storyLine,
                         "genre": genresList[genreIndex], "link": link}
                movieList.append(movie)
            if len(moviesLinkSet) % 50 == 0:
                break
    with open(movieJSONFileList[genreIndex], 'w') as f:
        f.write(json.dumps(movieList))
        f.close()
