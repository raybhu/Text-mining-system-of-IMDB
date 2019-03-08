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
import numpy as np

twenty_train = fetch_20newsgroups(subset='train')
twenty_test = fetch_20newsgroups(subset='test')
# Logistic Regression
# count_vect = CountVectorizer()
# X_train_counts = count_vect.fit_transform(twenty_train.data)
# tfidf_transformer = TfidfTransformer()
# X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
# clf = LogisticRegression().fit(X_train_tfidf, twenty_train.target)
# X_test_counts = count_vect.transform(twenty_test.data)
# X_test_tfidf = tfidf_transformer.transform(X_test_counts)
# predicted = clf.predict(X_test_tfidf)
# # for doc, category in zip(twenty_test.data, predicted):
# #     print('Classified as: %s\n%s\n' %
# #           (twenty_train.target_names[category], doc))

# print('Accuracy: %.3f\n' % np.mean(predicted == twenty_test.target))
# print(metrics.confusion_matrix(twenty_test.target, predicted))
# print(metrics.classification_report(twenty_test.target,
#                                     predicted, target_names=twenty_test.target_names))

# SVM
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(twenty_train.data)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
clf = SVC().fit(X_train_tfidf, twenty_train.target)
X_test_counts = count_vect.transform(twenty_test.data)
X_test_tfidf = tfidf_transformer.transform(X_test_counts)
predicted = clf.predict(X_test_tfidf)
