import re
import platform
import json
import os
import math
import pandas as pd
from pandas import ExcelWriter


def term_freq(word_list):
    word_dict = {}
    for w in word_list:
        if w in word_dict:
            word_dict[w] += 1
        else:
            word_dict[w] = 1
    word_num = float(sum(word_dict.values()))
    print(word_num)
    for w in word_dict.keys():
        word_dict[w] /= word_num
    return word_dict


def inv_doc_freq(term_set, doc_name2word_list):
    doc_num = len(doc_name2word_list)
    idf_dict = {}
    # term in all doc
    for w in term_set:
        doc_count = 0
        # find the appear frenquency among all documents
        for word_list in doc_name2word_list.values():
            if w in word_list:
                doc_count += 1
        idf_dict[w] = math.log(doc_num / doc_count)
    return idf_dict


if platform.system() == 'Darwin':
    movieFilteredJSONFile = './movies_filtered.json'
elif platform.system() == 'Windows':
    movieFilteredJSONFile = 'movies_filtered.json'
moviesNameList = []
moviesWordDict = {}
moviestfDict = {}
term_set = set()
with open(movieFilteredJSONFile, 'r') as f:
    movies = json.load(f)

for movie in movies:
    moviesNameList.append(movie['name'])
    moviesWordDict[movie['name']] = movie['storyline'].split()
    moviestfDict[movie['name']] = term_freq(movie['storyline'].split())
    # retuen union
    term_set = term_set | set(movie['storyline'].split())
    # print(moviesWordDict[movie['name']], moviestfDict[movie['name']])
    # print(term_set)
    # print(moviesNameList)
idf_dict = inv_doc_freq(term_set, moviesWordDict)
term_list = list(term_set)
tf_idf = pd.DataFrame(columns=moviesNameList, index=term_list)
count1 = 0
print(len(term_set))

for (movie, wordList) in moviesWordDict.items():
    count1 += 1
    print('count1=', count1)
    count2 = 0
    for w in term_set:
        count2 += 1
        print('count2=', count2)
        if w in wordList:
            tf_idf.loc[w, movie] = moviestfDict[movie][w] * idf_dict[w]
        else:
            tf_idf.loc[w, movie] = 0

writer = ExcelWriter('tfidf_result.xlsx')
tf_idf.to_excel(writer, 'tfidf')
writer.save()
print('File Output Success')
