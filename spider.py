import os
import requests
import argparse
import tushare as ts
import baostock as bs
from loguru import logger

tushare_token = '7daf71578ad8d18478b37df3bfcb02bc201b10134069f9afa6c94d44'


class StockSpider(object):

    def __init__(self, workdir: str) -> None:
        self.workdir = workdir
        self.ts_api = self.init_ts()
        self.bs_api = self.init_bs()

    def init_ts(self):
        ts.set_token(tushare_token)
        logger.info(f'login tushare success!')
        return ts.pro_api()

    def init_bs(self):
        bs.login()
        logger.info(f'login baostock success!')
        return bs

    def get_daliy_by_ts(self, code: str, start: str, end: str):
        self.ts_api.daily(ts_code=code, start_date=start, end_date=end)
        # self.ts_api.daily(ts_code='000001.SZ', start_date='19800701', end_date='20180718')

    def get_history_k_data(self, code: str,start:str,end:str):
        # self.bs_api.query_history_k_data_plus(
        #     "sh.600000",
        #     "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
        #     start_date='2017-07-01',
        #     end_date='2017-12-31',
        #     frequency="d",
        #     adjustflag="3",
        # )
        self.bs_api.query_history_k_data_plus(
            "sh.600000",
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
            start_date=start,
            end_date=end,
            frequency="d",
            adjustflag="3",
        )


if __name__ == '__main__':
    prog = 'python3 spider.py'
    description = ('data spider')
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument(
        '--code',
        type=str,
        help=f'stock code',
    )
    parser.add_argument(
        '--start',
        type=str,
        help='stock data start date',
    )
    parser.add_argument(
        '--end',
        type=str,
        help='stock data end date',
    )
    parser.add_argument(
        '--output',
        type=str,
        default='data/',
        help='stock data output path,default:data/stock_code/*',
    )

    args = parser.parse_args()

    code: str = args.code
    start: str = args.start
    end: str = args.end
    output: str = args.output
    os.makedirs(output, exist_ok=True)

    ss = StockSpider(output)