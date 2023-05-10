import requests
from requests.adapters import HTTPAdapter, Retry
import math

from settings import api_header

MAX_RETRY = 50


def merge_dictionaries(a: dict, b: dict):
    return {**a, **b}


def get_session():
    session = requests.Session()
    retries = Retry(total=MAX_RETRY, backoff_factor=1, status_forcelist=[403])
    session.mount('https://api.github.com', HTTPAdapter(max_retries=retries))

    return session


def get_from_pages(url, params={}, headers={}):
    session = get_session()
    headers = merge_dictionaries(headers, api_header)

    first_page = session.get(url, params=params, headers=headers).json()
    yield first_page

    next_page = first_page
    page = 0
    while len(next_page) == 100:
        page += 1
        next_page = session.get(url, params=merge_dictionaries(
            params, {'page': page}), headers=headers).json()
        yield next_page


def search(url, keyword, start_date, end_date):
    '''
    GitHub limits the number of search results that can be loaded by one search query (1000). This makes things tricky.
    This function uses the fact that the API does say howmany results there could be, even if it stopps returning them
    after the quota is reached. We just ask GitHub to sort the results by created_at and adjust the end date after the
    last (10th) page was loaded to begin with a new search query.
    '''
    session = get_session()

    while True:
        params = {
            'q': f'\"{keyword}\"+created:{start_date}..{end_date}', 'per_page': 100}
        first_page = session.get(url, params=params, headers=api_header).json()
        yield first_page

        num_pages = math.ceil(first_page['total_count'] / 100)
        for page in range(2, min([10 + 1, num_pages])):
            next_page = session.get(url, params=merge_dictionaries(
                params, {'page': page}), headers=api_header).json()
            yield next_page

        if num_pages <= 10:
            # No more timeframes to load. We are done with this one!
            return

        end_date = next_page['items'][-1]['created_at']
