import requests
from bs4 import BeautifulSoup as bs
from collections import OrderedDict


def get_seasons(url):

    main_page = requests.get(url)

    season_list = OrderedDict()

    main_page = bs(main_page.content.decode("utf-8"), "lxml")
    season_table = main_page.find("div", {'class': 'contents movies_small'})
    for each in season_table.find_all('a'):
        season_list[each.find('span', {'class': 'title'}).text] = each['href']

    return season_list
