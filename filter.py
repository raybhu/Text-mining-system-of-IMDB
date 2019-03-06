import platform
import json
import re
import shutil

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
            storyLine = re.sub(
                '[;:.,!?\-/+^\'_$%*()`~\"@#&={}\[\]|\\\\<>]', '', movie['storyline'])
            storyLine = storyLine.lower()
            stopwords = ('a', 'an', 'the', 'he', 'she', 'it')
            tokens = storyLine.split()
            tokens = [w for w in tokens if w not in stopwords]
            storyLine = ' '.join(tokens)
            name = re.sub('\((.*?)\)', '', movie['name'])
            tokens = name.split()
            name = ' '.join(tokens)
            moviesFilteredList.append(
                {"name": name, "storyline": storyLine, "link": movie['link']})
    f.write(json.dumps(moviesFilteredList))
    f.close()
