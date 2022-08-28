import os
import time
import json
import utils
import requests
import argparse
from bs4 import BeautifulSoup
from loguru import logger


class EastMoneySpider(object):
    def __init__(self, workdir: str):
        self.workdir = workdir

    def data_list_url(self, ):
        params = {
            'callback': 'jQuery1123043261808336536944_1661584908987',
            'sortColumns': 'SECURITY_CODE',
            'sortTypes': 1,  ##股票代码
            'pageSize': 300,
            'pageNumber': 1,
            'reportName': 'RPT_INDEX_TS_COMPONENT',
            'columns':
            'SECUCODE%2CSECURITY_CODE%2CTYPE%2CSECURITY_NAME_ABBR%2CCLOSE_PRICE%2CINDUSTRY%2CREGION%2CWEIGHT%2CEPS%2CBPS%2CROE%2CTOTAL_SHARES%2CFREE_SHARES%2CFREE_CAP',
            'quoteColumns': 'f2%2Cf3',
            'quoteType': 0,
            'source': 'WEB',
            'client': 'WEB',
            'filter': '(TYPE%3D%221%22)',
        }
        headers = {'Cookie': 'JSESSIONID=1189FCD4A6818D568A5962AD5A555E0C'}
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get?"
        return url, params, headers,

    def get_stock_data(self, ):
        stock_list_path = f'{self.workdir}/stock_data_list.json'
        if os.path.exists(stock_list_path):
            logger.info(
                f'stock list data {stock_list_path} is exist,skip download')
            return stock_list_path
        url, params, headers, = self.data_list_url()
        url = utils.url_set_params(url, params)
        logger.info(f'get stock data url:{url}')
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        prefix = len(params['callback']) + 1
        suffix = -2
        resp_data = resp.text[prefix:suffix]
        with open(stock_list_path, 'w') as f:
            json.dump(json.loads(resp_data), f, indent=4, ensure_ascii=False)
        return stock_list_path

    def get_stock_news_page(self, code: str):
        return 50

    def get_article_info(self, article):
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

    def get_html_articles_info(self, html_path: str, workdir: str):
        news_info_path = f'{workdir}/news_info.json'
        if os.path.exists(news_info_path):
            logger.info(f'news info {news_info_path} is exist,skip download')
            return news_info_path
        soup = BeautifulSoup(open(html_path), 'html.parser')
        articles = soup.findAll(attrs={'class': 'articleh normal_post'})
        article_infos = []
        for article in articles:
            article_info = self.get_article_info(article)
            article_infos.append(article_info)
        logger.info(f'html articles info save to {news_info_path}')
        with open(news_info_path, 'w') as f:
            json.dump(article_infos, f, indent=4, ensure_ascii=False)
        return news_info_path

    def stock_news_html(self, url: str, workdir: str):
        os.makedirs(workdir, exist_ok=True)
        news_html_path = f'{workdir}/news.html'
        news_info_path = f'{workdir}/news_info.json'
        if os.path.exists(news_html_path) and os.path.exists(news_info_path):
            logger.info(f'skip download url')
            return
        utils.get_html(url, news_html_path)
        try:
            self.get_html_articles_info(news_html_path, workdir)
            time.sleep(10)
        except Exception as e:
            logger.error(f'workdir:{workdir},error:{e}')

    def stokc_news_spider(
            self,
            code: str,
    ):
        news_page = self.get_stock_news_page(code)
        stock_workdir = f'{self.workdir}/news/{code}'
        for index in range(1, news_page + 1):
            url = f'https://guba.eastmoney.com/list,{code},f_{index}.html'
            logger.info(f'stock:{code},html index:{index},url:{url}')
            self.stock_news_html(url, f'{stock_workdir}/{index}')

    def run(self):
        data_list_path = self.get_stock_data()
        with open(data_list_path, 'r') as f:
            data_info = json.load(f)
        logger.info(f'eastmoney data list version:{data_info["version"]}')
        for stock in data_info['result']['data']:
            stock_code = stock['SECURITY_CODE']
            stock_name = stock['SECURITY_NAME_ABBR']
            logger.info(f'catch stock:{stock_code},name:{stock_name}')
            self.stokc_news_spider(stock_code)


if __name__ == '__main__':
    prog = 'python3 eastmoney.py'
    description = ('eastmoney data spider')
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument(
        '--workdir',
        type=str,
        default='data/eastmoney',
        help='spider data workdir',
    )

    args = parser.parse_args()
    workdir: str = args.workdir
    os.makedirs(workdir, exist_ok=True)
    eastmoney = EastMoneySpider(workdir)
    eastmoney.run()
