from __future__ import print_function
import requests
import json
import platform
import re
import shutil
from bs4 import BeautifulSoup
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from sklearn.metrics import pairwise_distances
from sklearn.cluster import KMeans
from wordcloud import WordCloud

# path
if platform.system() == 'Darwin':
    movieJSONFile = './movies.json'
elif platform.system() == 'Windows':
    movieJSONFile = 'movies.json'
if platform.system() == 'Darwin':
    movieFilteredJSONFile = './movies_filtered.json'
elif platform.system() == 'Windows':
    movieFilteredJSONFile = 'movies_filtered.json'
# crawler
topMovieListURL = 'https://www.imdb.com/chart/top?ref_=nv_mv_250'
topMovieListHtml = requests.get(topMovieListURL)
bs = BeautifulSoup(topMovieListHtml.text, 'lxml')
movieListTable = bs.find_all('td', {'class': 'titleColumn'})
movieList = []
for index, movieLink in enumerate(movieListTable[0:100]):
    print('The crawler is working on %d movie.' % (index+1))
    link = 'https://www.imdb.com' + movieLink.find('a')['href'] + '/'
    html = BeautifulSoup(requests.get(link).text, 'lxml')
    name = html.find('h1').text

    storyLine = html.find('div', {'id': 'titleStoryLine'}).find(
        'div', {'class': 'inline canwrap'}).find('span').text
    movie = {"name": name, "storyline": storyLine, "link": link}
    movieList.append(movie)
with open(movieJSONFile, 'w') as f:
    f.write(json.dumps(movieList))
    f.close()
print('The original movie information has been saved in movies_filtered.json.')
# filter


def stopword_filtered(words):
    filtered_list = []
    stop_set = set(stopwords.words('english'))
    # print(stop_set)
    for w in words:
        if w not in stop_set:
            filtered_list.append(w)
    return filtered_list


with open(movieJSONFile, 'r') as f:
    movies = json.load(f)
moviesFilteredList = []
for index, movie in enumerate(movies):
    print('The filter is working on %d movie.' % (index+1))
    if movie['storyline'] is not None:
        storyLine = movie['storyline'].lower()
        storyLine = stopword_filtered(storyLine.split())
        storyLine = ' '.join(storyLine)
        storyLine = re.sub(
            '[;:.,!?\-/+^\'_$%*()`~\"@#&={}\[\]|\\\\<>]', '', storyLine)
        name = re.sub('\((.*?)\)', '', movie['name'])
        name = name.strip()
        moviesFilteredList.append(
            {"name": name, "storyline": storyLine, "link": movie['link']})
with open(movieFilteredJSONFile, 'w') as f:
    f.write(json.dumps(moviesFilteredList))
    f.close()
print('The filtered movie information has been saved in movies.json.')
# transformer
with open(movieFilteredJSONFile, 'r') as f:
    movies = json.load(f)
storyLines = []
for movie in movies:
    storyLines.append(movie['storyline'])
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(storyLines)
ks = [10, 15, 20]
score = 0
k = 0
for kCache in ks:
    print('transformer is testing appropriate k value.')
    km = KMeans(n_clusters=kCache)
    kmeans_model = km.fit(X)
    km.fit_transform(X)
    labels = kmeans_model.labels_
    scoreCache = metrics.silhouette_score(X, labels, metric='euclidean')
    print('The k Value is %d, and the corresponding silhouette coefficient is %f.' %
          (kCache, scoreCache))
    if scoreCache > score:
        score = scoreCache
        k = kCache
print('The tranformer has picked out best k value and calculated silhouette score, which are %d and %f. ' % (k, score))
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(0, k):
    # print('\n Cluster %d: ' % i, end='')
    wordList = []
    print('The transformer is generating %d wordcloud image.' % (i+1))
    for ind in order_centroids[i]:
        # print(' %s' % terms[ind], end='')
        wordList.append(terms[ind])
    wordcloud = WordCloud().generate(' '.join(wordList))
    wordcloud.to_file('./wordcloud/cluster'+str(i+1)+'.png')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
print('The wordcloud images has been saved in wordcloud folder.')
