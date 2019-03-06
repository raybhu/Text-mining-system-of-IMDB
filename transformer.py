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


if platform.system() == 'Darwin':
    movieFilteredJSONFile = './movies_filtered.json'
elif platform.system() == 'Windows':
    movieFilteredJSONFile = 'movies_filtered.json'
with open(movieFilteredJSONFile, 'r') as f:
    movies = json.load(f)
    for movie in movies[0:1]:
        print(term_freq(movie['storyline'].split()))
