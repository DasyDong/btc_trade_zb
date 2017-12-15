from datetime import datetime, timedelta
from urllib import urlencode
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError


def get_page_data(from_city, to_city, offset):
    start_date = datetime.strptime("2017-02-24", "%Y-%m-%d") \
                  + timedelta(days=offset)
    data = {
        'from': from_city,
        'to': to_city,
        'date': start_date
    }
    params = urlencode(data)
    base = 'http://flights.ctrip.com/booking/'
    url = base + '?' + params
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        print('Error occurred')
        return None


def parse_page_detail(text):
    bs = BeautifulSoup(text, 'html.parser')
    elements = bs.find_all('span', class_='low_price')
    return min([ele.text for ele in elements])


def price(offset):
    text = get_page_data('she', 'sha', offset)
    return parse_page_detail(text), offset


def main():
    print map(price, range(7))
