import requests
from bs4 import BeautifulSoup as bs


def get_episodes(chosen_season):

    res = requests.get(chosen_season)

    res = bs(res.content.decode('utf-8'), "lxml")

    x = res.find('div', {'class': 'movies_small'})
    episodes_list = []
    for each in x.find_all('a'):
        episodes_list.append(str(each['href']))

    episodes_list.reverse()

    return episodes_list
