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
import json


if platform.system() == 'Darwin':
    movieJSONFileList = ['./movies_biography.json',
                         './movies_action.json', './movies_comedy.json']
elif platform.system() == 'Windows':
    movieJSONFileList = ['movies_biography.json',
                         'movies_action.json', 'movies_comedy.json']
genresList = ['biography', 'action', 'comedy']
# moviesDict = {}
targetList = []
storyLineTrainList = []
storyLineTestList = []
for index, path in enumerate(movieJSONFileList):
    genreIndex = index
    with open(path, 'r') as f:
        movies = json.load(f)
    for movie in movies[0:25]:
        storyLineTrainList.append(movie['storyline'])
        targetList.append(str(genreIndex))
    for movie in movies[25:50]:
        storyLineTestList.append(movie['storyline'])
target = np.array(targetList)
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(storyLineTrainList)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
clf = SVC(gamma='auto')
clf.fit(X_train_tfidf, target)
X_test_counts = count_vect.transform(storyLineTestList)
X_test_tfidf = tfidf_transformer.transform(X_test_counts)
predicted = clf.predict(X_test_tfidf)

df = pd.DataFrame(metrics.classification_report(target,
                                                predicted, target_names=genresList, output_dict=True)).transpose()
writer = ExcelWriter('Bonus_SVM_results.xlsx')
df.to_excel(writer, 'SVM')
writer.save()
print('Accuracy: %.3f\n' % np.mean(predicted == target))
print(metrics.confusion_matrix(target, predicted))
