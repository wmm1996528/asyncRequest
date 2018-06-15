import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('spiders')

# 线程数量
THREADBOOL = False  # True 开启多线程
THREADNUM = 10  # 设定多线程数量

# 代理IP
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}
PROXYIP = False
# 配置 urls
URLS = ['http://sou.zhaopin.com/jobs/searchresult.ashx?in=160400&jl=%E5%8C%97%E4%BA%AC&p={}&isadv=0'.format(i) for i in
        range(100)]
# s = urls.find({}).limit(2)
# for i in s:
#     URLS.append(i['url'])
# 解析规则
REGULARS = {

}

XPAHTS = {
    'name': '//*[@id="newlist_list_content_table"]/table/tr[1]/td[1]/div/a/text()',
    'companys_name': '//*[@id="newlist_list_content_table"]/table/tr[1]/td[3]/a[1]/text()',
    'price': '//*[@id="newlist_list_content_table"]/table/tr[1]/td[4]/text()',
}

# redis 路径
REDIS_URL = "redis://47.98.165.242:6379"
# mongo 路径
MONGO_URL = 'mongodb://127.0.0.1:27017'
