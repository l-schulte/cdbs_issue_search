import requests
from requests.adapters import HTTPAdapter, Retry
import math

from settings import api_header

MAX_RETRY = 50

def merge_dictionaries(a: dict, b: dict):
    return {**a, **b}

def get_session():
    session = requests.Session()
    retries = Retry(total=MAX_RETRY, backoff_factor=1, status_forcelist=[ 403 ])
    session.mount('https://api.github.com', HTTPAdapter(max_retries=retries))

    return session

def get_from_pages(url, params = {}, headers = {}):
    session = get_session()
    headers = merge_dictionaries(headers, api_header)
    
    first_page = session.get(url, params=params, headers=headers).json()
    yield first_page

    def get_next(page):
        return session.get(url, params=merge_dictionaries(params, {'page': page}), headers=headers).json()


    if (isinstance(first_page, list)):
        next_page = first_page
        page = 0
        while len(next_page) > 0:
            page += 1
            next_page = get_next(page)
            yield next_page
    else:
        num_pages = math.ceil(first_page['total_count'] / 100)
        print(f'results #pages: {num_pages}')
        for page in range(2, num_pages + 1):
            next_page = get_next(page)
            yield next_page