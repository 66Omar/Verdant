import requests
from bs4 import BeautifulSoup as bs
from collections import OrderedDict
from Scraping.get_link import get_link


search = get_link()


def search_for(name):

    search_result = requests.get(search + name)

    search_result = bs(search_result.content.decode("utf-8"), "lxml")
    items_list = OrderedDict()

    for item in search_result.find_all('a', {'class': "movie"}):
        img = item.find('img')
        title = item.find("span", {'class': 'title'})
        try:
            quality = item.find('span', {'class': 'ribbon'}).text
        except AttributeError:
            quality = 'Unknown'
        items_list[title.text] = [item['href'], img['src'], quality]

    return items_list
