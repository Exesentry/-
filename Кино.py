from bs4 import BeautifulSoup

import requests


def all_cinema():
    b = requests.get('https://kinoteatr.ru/raspisanie-kinoteatrov/')
    for _ in BeautifulSoup(b.text, 'lxml').find_all('div', {'class': 'cinema_card'}):
        yield _.find('a').attrs['href'], \
              _.find('h3', {'class': 'movie_card_title'}).text.strip(), \
              _.find('span', {'class': 'sub_title'}).text.strip()


def all_films(cinema_url):
    cinema = requests.get(cinema_url)
    for _ in BeautifulSoup(cinema.text, 'lxml').find_all('div', {'class': 'shedule_movie'}):
        yield _.attrs['data-gtm-list-item-filmname'], \
              _.find('a', {'class': 'gtm-ec-list-item-movie'}).attrs['href'], \
              _.attrs['data-gtm-format'], \
              _['data-gtm-list-item-genre'], \
              _.find('i', {'class': 'raiting_sub'}).text


for cinema_link, cinema_name, cinema_address in all_cinema():
    print('Кинотеатр "{}"(Адрес: {})\nФильмы в кинотеатре:'.format(cinema_name, cinema_address))
    for film_name, film_link, frmt, genre, raiting in all_films(cinema_link):
        print('Название фильма: "{}" {}, Жанр: {}, Возрастное ограничение: {}\nСсылка:{}'.format(
            film_name, frmt, genre, raiting, film_link))
    print('\n------------------------------------\n')
