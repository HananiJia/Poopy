import os
import re
import json
import requests
from bs4 import BeautifulSoup
from loguru import logger


def get_html(url: str, path: str):
    if os.path.exists(path):
        logger.info(f'url {path} is exists,skip download')
        return
    resp = requests.get(url)
    resp.raise_for_status()
    with open(path, 'w') as f:
        f.write(resp.text)


def parser_article_html(html_path: str):
    article_info = {}
    soup = BeautifulSoup(open(html_path), 'html.parser')
    article_info['title'] = soup.head.title.text
    post_content = soup.find(attrs={'class': 'stockcodec .xeditor'})
    article_info['content'] = post_content.text.strip()
    user_data = soup.find(attrs={'class': 'data'})
    article_info['user'] = user_data['data-json']
    post_time = soup.find(attrs={'class': 'zwfbtime'})
    post_info_list = post_time.text.strip().split(" ")
    article_info['time'] = {
        'time': f'{post_info_list[1]} {post_info_list[2]}',
        'platform': post_info_list[3]
    }
    article_info['type'] = 'common'
    return article_info


def parser_caifuhao_html(html_path: str):
    article_info = {}
    soup = BeautifulSoup(open(html_path), 'html.parser')
    article_info['title'] = soup.head.title.text
    post_content = soup.find(attrs={'class': 'xeditor_content'})
    if not post_content:
        post_content = soup.find(
            attrs={'class': 'xeditor_content editorlungo_content'})
    article_info['content'] = post_content.text
    article_meta = soup.find(attrs={'class': 'article-meta'})
    for span in article_meta.findAll('span'):
        if span.get('id') == 'authorwrap':
            article_info['user'] = {
                'user_id': span['data-uid'],
                'user_nickname': span.text.strip(),
            }
        elif 'txt' in span['class']:
            article_info['time'] = {'time': span.text, 'platform': 'Web'}

    article_info['type'] = 'caifuhao'
    return article_info


def get_article_details(info):
    href = info['href']
    article_html_path = f'{info["title"]}.html'
    if 'caifuhao.eastmoney.com' in href:
        url = f'https:{href}'
    else:
        url = f'https://guba.eastmoney.com{href}'
    try:
        get_html(url, article_html_path)
        if 'caifuhao.eastmoney.com' in href:
            article_details = parser_caifuhao_html(article_html_path)
        else:
            article_details = parser_article_html(article_html_path)
        return article_details
    except Exception as e:
        logger.error(e)
        return None


article_info_path = '/home/haonan/code/chenghong/Poopy/data/eastmoney/news/000001/1/news_info.json'

with open(article_info_path, 'r') as f:
    article_infos = json.load(f)

infos = []
for article_info in article_infos:
    a_info = get_article_details(article_info)
    if not a_info:
        continue
    infos.append(a_info)
print(infos)
with open('infos.json', 'w') as f:
    json.dump(infos, f, indent=4, ensure_ascii=False)
