import requests
from bs4 import BeautifulSoup as bs
from collections import OrderedDict


search = 'https://beal.egybest.xyz/explore/?q='


def search_for(name):

    search_result = requests.get(search + name)

    search_result = bs(search_result.content.decode("utf-8"), "lxml")
    items_list = OrderedDict()

    for item in search_result.find_all('a', {'class': "movie"}):
        title = item.find("span", {'class': 'title'})
        items_list[title.text] = item['href']

    return items_list
