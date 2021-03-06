"""
配置文件
可以配置线程，代理，解析规则，数据库路径
"""
import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('spiders')

# 线程数量
THREADBOOL = False  # True 开启多线程
THREADNUM = 10  # 设定多线程数量

# 代理IP
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}
PROXYIP = True

proxies = {}

n = 0


def get_ip():
    global n
    url = 'http://tvp.daxiangdaili.com/ip/?tid=556862908033437&num=1&category=2&protocol=https'
    ip = requests.get(url).text
    proxy = {
        'http': ip,
        'https': ip,
    }
    n += 1
    print('第%s次' % n)
    return proxy


if PROXYIP is True:
    proxies = get_ip()
# 配置 urls
URLS = ['http://sou.zhaopin.com/jobs/searchresult.ashx?in=160400&jl=%E5%8C%97%E4%BA%AC&p={}&isadv=0'.format(i) for i in
        range(500)]
# URLS = ['http://httpbin.org/ip'] * 1000
# print(len(URLS))
# s = urls.find({}).limit(2)
# for i in s:
#     URLS.append(i['url'])
# 解析规则
REGULARS = {

}

XPAHTS = {
    'name': '//*[@id="newlist_list_content_table"]/table/tr[1]/td[1]/div/a/text()',
    'company_name': '//*[@id="newlist_list_content_table"]/table/tr[1]/td[3]/a[1]/text()',
    'price': '//*[@id="newlist_list_content_table"]/table/tr[1]/td[4]/text()',
}

# redis 路径
REDIS_URL = "redis://127.0.0.1:6379"
# mongo 路径
MONGO_URL = 'mongodb://127.0.0.1:27017'

# 分布式
Distributed = True
DistributedNum = 100
