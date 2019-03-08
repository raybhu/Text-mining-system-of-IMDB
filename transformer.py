from __future__ import print_function
import json
import numpy as np
import platform
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from sklearn.metrics import pairwise_distances
from sklearn.cluster import KMeans
from wordcloud import WordCloud
import matplotlib.pyplot as plt

if platform.system() == 'Darwin':
    movieFilteredJSONFile = './movies_filtered.json'
elif platform.system() == 'Windows':
    movieFilteredJSONFile = 'movies_filtered.json'

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
    km = KMeans(n_clusters=kCache)
    kmeans_model = km.fit(X)
    km.fit_transform(X)
    labels = kmeans_model.labels_
    scoreCache = metrics.silhouette_score(X, labels, metric='euclidean')
    if scoreCache > score:
        score = scoreCache
        k = kCache
    print(score)
    print(k)
print('Top terms per cluster:')
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
# WordCloudTextList = []
for i in range(0, k):
    print('\n Cluster %d: ' % i, end='')
    wordList = []
    for ind in order_centroids[i]:
        print(' %s' % terms[ind], end='')
        wordList.append(terms[ind])

    wordcloud = WordCloud().generate(' '.join(wordList))
    wordcloud.to_file('./wordcloud/cluster'+str(i+1)+'.png')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
