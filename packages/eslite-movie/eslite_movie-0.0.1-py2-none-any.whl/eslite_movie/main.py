import requests

from .const import URL
from .crawler import EsliteMovieCrawler

def GetMovies():
    req = requests.get(URL)
    eslite = EsliteMovieCrawler(req.content.decode('utf8'))

    return eslite.movie_list()
