import requests
from bs4 import BeautifulSoup
import csv
import os



URL = 'https://www.olx.uz/transport/legkovye-avtomobili/chevrolet/cobalt/tashkent/?search%5Bfilter_enum_condition%5D%5B0%5D=perfect&search%5Bfilter_enum_condition%5D%5B1%5D=good&search%5Bfilter_enum_condition%5D%5B2%5D=mediocre&search%5Bphotos%5D=1&search%5Border%5D=created_at%3Adesc'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'accept': '*/*'}
FILE = 'cars.csv'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='item fleft')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='offer-wrapper')

    cars = []

    for item in items:
        cars.append({
            'image': item.find('img', class_='fleft').get('src'),
            'title': item.find('h3', class_='lheight22 margintop5').get_text(strip=True),
            'link_to_post': item.find('a', class_='marginright5').get('href'),
            'price': item.find('p', class_='price').get_text(strip=True),
            'city': item.find('small', class_='breadcrumb x-normal').find_next('span').get_text(strip=True),
            })

    return cars


def save_file(items, path):
    with open('cars.csv', mode='a', encoding='utf8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Rasmi',
                         'Markasi',
                         "E'lon ssilkasi",
                         'Narxi',
                         'Shahar'])
        for item in items:
            writer.writerow([item['image'],
                             item['title'],
                             item['link_to_post'],
                             item['price'],
                             item['city']])


def parse():
    URL = input('Please enter the URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Parsing page: {page} from {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        save_file(cars, FILE)
        print(f' Received {len(cars)} cars')
        os.startfile(FILE)
    else:
        print('ERROR')


parse()
