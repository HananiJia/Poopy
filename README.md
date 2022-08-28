# Poopy
    运行环境：python 3.6+

tushare : https://tushare.pro/document/2

daily

ts_code trade_date  open  high  ...  change  pct_chg         vol       amount
0   000001.SZ   20180718  8.75  8.85  ...   -0.02    -0.23   525152.77   460697.377
1   000001.SZ   20180717  8.74  8.75  ...   -0.01    -0.11   375356.33   326396.994
2   000001.SZ   20180716  8.85  8.90  ...   -0.15    -1.69   689845.58   603427.713
3   000001.SZ   20180713  8.92  8.94  ...    0.00     0.00   603378.21   535401.175

[13 rows x 11 columns]


Baostock : http://baostock.com/baostock/index.php/Python_API%E6%96%87%E6%A1%A3



## 数据抓取模块
一、东方财富【股吧全部内容】
沪深300
http://guba.eastmoney.com/list,zssz399300.html
http://guba.eastmoney.com/list,zssh000300.html
沪深300成分股（可根据此列表得到其他股票代码）
https://data.eastmoney.com/other/index/
举例：平安银行（URL中list,股票代码）
http://guba.eastmoney.com/list,000001.html

二、新浪财经【网友讨论和公司新闻】
万科A（URL中name=股票代码） 
https://guba.sina.com.cn/?s=bar&name=sz000002

三、微博【全部内容】
举例：平安银行股票代码sz000001
https://s.weibo.com/weibo?q=sz000001