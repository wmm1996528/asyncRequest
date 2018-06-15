from multiprocessing.managers import BaseManager
from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParser
from my_wokres.DataOutput import DataOutput


class SpiderWorker():
    def __init__(self):
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')

        server_adrr = '127.0.0.1'
        print('connect to %s...' % server_adrr)

        self.m = BaseManager(address=(server_adrr, 8001), authkey=b'qiye')

        self.m.connect()
        self.task = self.m.get_task_queue()
        self.result = self.m.get_result_queue()
        self.downloader = HtmlDownloader()
        self.htmlparser = HtmlParser()
        self.dataoutput = DataOutput()

    def crawl(self):

        while True:
            try:
                if self.task.empty:
                    url = self.task.get()
                    if url == 'end':
                        return None
                    print('正在解析 %s' % url.encode('utf-8'))
                    content = self.downloader.download(url)
                    new_urls, data = self.htmlparser.parser(url, content)
                    self.result.put({'new_urls': new_urls})
                    self.dataoutput.output_mongo({'data': data})
            except Exception as e:
                print(e)


if __name__ == '__main__':
    spider = SpiderWorker()
    spider.crawl()

';glXb-hPh8.b'

'''
sudo rm /usr/local/mysql
sudo rm -rf /usr/local/mysql*
sudo rm -rf /Library/StartupItems/MySQLCOM
sudo rm -rf /Library/PreferencePanes/My*
vim /etc/hostconfig  (and removed the line MYSQLCOM=-YES-)
rm -rf ~/Library/PreferencePanes/My*
sudo rm -rf /Library/Receipts/mysql*
sudo rm -rf /Library/Receipts/MySQL*
sudo rm -rf /var/db/receipts/com.mysql.*'''
