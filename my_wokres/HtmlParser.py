from my_wokres.DataOutput import DataOutput
from my_wokres import RedisWorker
from lxml import etree
import traceback
from my_wokres import RedisWorker
from my_wokres.DataOutput import DataOutput
from setting import *

BASE_URL = 'https://www.guazi.com'


class HtmlParser(object):
    def __init__(self):
        self.r = RedisWorker.redisQueue('new')
        self.data = DataOutput()

    def parser(self, url, htmls):
        '''
        解析网页
        :param page_url: url
        :param html_cont: content
        :return: url 和数据
        '''
        if htmls == None:
            return
        try:
            h = etree.HTML(htmls)
        except:
            h = etree.fromstring(htmls)
        # res =
        res = self._get_datas(url, h)
        return res
    def _get_datas(self, url, html):
        try:
            data = {}
            for i in XPAHTS.items():
                name = i[0]
                paths = i[1]
                try:
                    names = html.xpath(paths)[0]
                except:
                    names = 'NULL'
                data.update({
                    name: names
                })
            return  data
        except Exception as e:
            logger.warning(traceback.format_exc())


if __name__ == '__main__':
    s = HtmlParser()
    f = open('1.html').read()
    s.parser(b'no', f)
