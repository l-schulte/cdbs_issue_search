import requests
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from time import sleep
import os

from settings import private_token

GITHUB_KEY = private_token
MAX_RESULTS = 100

rate_limit_bar = tqdm(desc="Ratelimit")


def __handle_ratelimit(response):
    global rate_limit_bar

    rate_limit_bar.n = int(response.headers['x-ratelimit-remaining'])
    rate_limit_bar.total = int(response.headers['x-ratelimit-limit'])
    rate_limit_bar.refresh()

    if int(response.headers['x-ratelimit-remaining']) == 0:
        sleep(int(response.headers['x-ratelimit-reset']) -
              datetime.now().timestamp() + 10)


def response_generator(url):
    page = 0

    while True:
        page += 1
        response = requests.get(
            url + f"&page={page}&per_page={MAX_RESULTS}",
            headers={'Authorization': f'Bearer {GITHUB_KEY}'}
        )

        if not response.ok:
            # print(f'{response.status_code}, {response.reason} at {response.url}')
            return []

        data = response.json()
        for issue in data:
            yield issue

        __handle_ratelimit(response)

        if len(data) < MAX_RESULTS:
            return
