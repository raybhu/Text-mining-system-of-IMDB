import re
import platform
import json
import os
import math
import pandas as pd
from pandas import ExcelWriter

if platform.system() == 'Darwin':
    movieJSONFile = './movies.json'
elif platform.system() == 'Windows':
    movieJSONFile = 'movies.json'
with open(movieJSONFile, 'r') as f:
    movies = json.load(f)
    for movie in movies:
        print(movie['storyline'])


def term_freq(word_list):
    word_dict = {}
    for w in word_list:
        if w in word_dict:
            word_dict[w] += 1
        else:
            word_dict[w] = 1
    word_num = float(sum(word_dict.values()))
    for w in word_dict.keys():
        word_dict[w] /= word_num
    return word_dict
