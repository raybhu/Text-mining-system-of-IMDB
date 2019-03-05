import requests
from bs4 import BeautifulSoup
movieListURL = 'https://www.imdb.com/chart/top?ref_=nv_mv_250'
htmlList = requests.get(movieListURL)
bs = BeautifulSoup(htmlList.text, 'lxml')
