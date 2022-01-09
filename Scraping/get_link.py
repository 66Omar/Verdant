import requests
from bs4 import BeautifulSoup as bs


URL = 'https://www.egyverdant.tk/'


def get_link():
    request = requests.get(URL)
    link = bs(request.content, 'lxml')
    return link.find('body').text
