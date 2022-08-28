import os
from loguru import logger
import requests


def url_set_params(url: str, params: dict):
    for k, v in params.items():
        url += f'{k}={v}&'
    url = url[:-1]
    return url


def get_html(url: str, path: str):
    if os.path.exists(path):
        logger.info(f'url {path} is exists,skip download')
        return
    resp = requests.get(url)
    resp.raise_for_status()
    with open(path, 'w') as f:
        f.write(resp.text)
