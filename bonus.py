import platform
from bs4 import BeautifulSoup
import requests
biographyLink = 'https://www.imdb.com/search/title?genres=biography'
actionLink = 'https://www.imdb.com/search/title?genres=action'
comedyLink = 'https://www.imdb.com/search/title?genres=comedy'
linkList = [biographyLink, actionLink, comedyLink]
if platform.system() == 'Darwin':
    movieJSONFile = './movies_orderbygenres.json'
elif platform.system() == 'Windows':
    movieJSONFile = 'movies_orderbygenres.json'

for link in linkList:
    html = requests.get(link)
    bs = BeautifulSoup(html.text, 'lxml')
