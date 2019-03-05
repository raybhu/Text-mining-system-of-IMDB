import requests
import json
import platform
from bs4 import BeautifulSoup


class Movie(object):
    def __init__(self, movieName, storyLine, link):
        self.movieName = movieName
        self.storyLine = storyLine
        self.link = link


topMovieListURL = 'https://www.imdb.com/chart/top?ref_=nv_mv_250'
topMovieListHtml = requests.get(topMovieListURL)
bs = BeautifulSoup(topMovieListHtml.text, 'lxml')
movieListTable = bs.find_all('td', {'class': 'titleColumn'})
movieList = []
for movieLink in movieListTable[0:100]:
    link = 'https://www.imdb.com' + movieLink.find('a')['href'] + '/'
    html = BeautifulSoup(requests.get(link).text, 'lxml')
    name = html.find('h1').text
    storyLine = html.find('div', {'id': 'titleStoryLine'}).find(
        'div', {'class': 'inline canwrap'}).find('span').text
    movie = {"name": name, "storyline": storyLine, "link": link}
    movieList.append(movie)
    # print(movie.movieName, movie.storyLine, movie.link)

movieJSONFile = ''
if platform.system() == 'Darwin':
    movieJSONFile = './movies.json'
elif platform.system() == 'Windows':
    movieJSONFile = 'movies.json'

with open(movieJSONFile, 'w') as f:
    f.write(json.dumps(movieList))
    f.close()
