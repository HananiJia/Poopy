import os
import time
import json
import requests
import argparse
from bs4 import BeautifulSoup
from loguru import logger


def get_article_info(article):
    article_info = {}
    for span in article.findAll('span'):
        if 'l1' in span['class']:
            article_info['reading_num'] = span.contents[0]
        elif 'l2' in span['class']:
            article_info['comments_num'] = span.contents[0]
        elif 'l3' in span['class']:
            for a_info in span.findAll('a'):
                a_keys = list(a_info.attrs.keys())
                if 'title' not in a_keys:
                    continue
                article_info['href'] = a_info['href']
                article_info['title'] = a_info['title']
        elif 'l4' in span['class']:
            article_info['author'] = span.font.text
        elif 'l5' in span['class']:
            article_info['time'] = span.contents[0]
        else:
            logger.warning(f'get article info calss:{span["class"]}')
    return article_info


html_path = '/home/haonan/code/chenghong/Poopy/data/eastmoney/news/000001/13/news.html'
soup = BeautifulSoup(open(html_path), 'html.parser')
articles = soup.findAll(attrs={'class': 'articleh normal_post'})
article_infos = []
for article in articles:
    article_info = get_article_info(article)
    article_infos.append(article_info)

with open('test_info.json', 'w') as f:
    json.dump(article_infos, f, indent=4, ensure_ascii=False)
