import requests
from bs4 import BeautifulSoup as bs
from collections import OrderedDict


def get_seasons(url, name):

    main_page = requests.get(url)

    season_list = OrderedDict()

    main_page = bs(main_page.content.decode("utf-8"), "lxml")
    season_table = main_page.find("div", {'class': 'contents movies_small'})
    for each in season_table.find_all('a'):
        season_list[translate(str(each.find('span', {'class': 'title'}).text).strip(name))] = each['href']
    return season_list


numbers = {
    "الاول": 'One',
    "الثانى": 'Two',
    "الثالث": 'Three',
    "الرابع": 'Four',
    "الخامس": "Five",
    "السادس": "Six",
    "السابع": 'Seven',
    'الثامن': 'Eight',
    "التاسع": "Nine",
    "العاشر": "Ten",
    "الحادي عشر": "Eleven",
    "الثاني عشر": "Twelve",
    "الثالث عشر": "Thirteen",
    "الرابع عشر": "Fourteen",
    "الخامس عشر": 'Fiveteen',
    "السادس عشر": "Sixteen",
    "السابع عشر": 'Seventeen',
    "الثامن عشر": 'Eighteen',
    "التاسع عشر": "Nineteen",
    "العشرون عشر": "Twenty",
}


def translate(text):
    try:
        temp = text.replace("الموسم", "").replace(" ", "").replace("'", "")
        new = numbers[temp]
        return f"Season {new}"
    except Exception:
        pass
    return text.replace("الموسم", "Season")
