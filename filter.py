import platform
import json
import re
import shutil
import nltk
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

# nltk.download('stopwords')


def stopword_filtered(words):
    filtered_list = []
    stop_set = set(stopwords.words('english'))
    # print(stop_set)
    for w in words:
        if w not in stop_set:
            filtered_list.append(w)
    return filtered_list


if platform.system() == 'Darwin':
    movieJSONFile = './movies.json'
elif platform.system() == 'Windows':
    movieJSONFile = 'movies.json'
with open(movieJSONFile, 'r') as f:
    movies = json.load(f)
if platform.system() == 'Darwin':
    movieFilteredJSONFile = './movies_filtered.json'
elif platform.system() == 'Windows':
    movieFilteredJSONFile = 'movies_filtered.json'
with open(movieFilteredJSONFile, 'w') as f:
    moviesFilteredList = []
    for movie in movies:
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
    f.write(json.dumps(moviesFilteredList))
    f.close()
