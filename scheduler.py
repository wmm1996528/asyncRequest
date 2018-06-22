import my_wokres.RedisWorker
from my_wokres.HtmlDownloader import HtmlDownloader
from my_wokres.HtmlParser import HtmlParser
from my_wokres.DataOutput import DataOutput
from app.monitoring import app
from threading import Thread
from setting import *
import time
import sys
import asyncio
import queue
import os

q = queue.Queue()
for i in URLS:
    q.put(i)


def costTime(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        func(*args, **kwargs)
        t2 = time.time()
        print(t2 - t1)

    return wrapper


sys.path.append("..")


class Spiders(object):
    def __init__(self):
        self.r = my_wokres.RedisWorker.redisQueue('new')
        self.html = HtmlDownloader()
        self.parser = HtmlParser()
        self.dataout = DataOutput()
        self.r.put(URLS)
        self.app = app
    def start(self):
        while self.r.get_size() != 0:
            url = self.r.get_wait()

            html = self.html.downnload_not_wait(url)
            # print(html)
            data = self.parser.parser(url, html)
            print(data)
            self.dataout.output_mongo(data)

    def process_start(self):
        process = []
        for thread in range(THREADNUM):
            p = Thread(target=self.start, args=())
            process.append(p)
        for thread in range(THREADNUM):
            logger.info('Process %s running........' % thread)
            process[thread].start()
        for thread in range(THREADNUM):
            process[thread].join()
            logger.info('Process %s completed........' % thread)

    def cost(self, data):
        while True:
            allUrl = self.r.get_size()
            now = self.r.get_old()
            time.sleep(10)
            after = self.r.get_old()
            # print(now, after)
            speed = after - now
            wait = allUrl - now
            print(wait)
            # print(allUrl - after)
            # print(speed)
            if wait == 0:

                try:
                    scheduledTime = str((allUrl - after) // speed)
                except:
                    scheduledTime = '已完成'
                data.update({
                    'timeNum': scheduledTime + '秒',
                    'progess': str(round((after / allUrl) * 100, 3)),
                    'nowNum': after,
                    'wait': wait
                })
                self.r.set_monit(data)
                os._exit(0)
                break
            else:
                try:
                    scheduledTime = str((allUrl - after) // speed)
                except ZeroDivisionError:
                    scheduledTime = 'weizhi'
                data.update({
                    'timeNum': scheduledTime + '秒',
                    'progess': str(round((after / allUrl) * 100, 3)),
                    'nowNum': after,
                    'wait': wait
                })
                self.r.set_monit(data)

    def start_monit(self):
        self.app.run(port=2121)

    @costTime
    def run(self):
        p = Thread(target=self.start_monit, args=())
        p.start()
        data = {}
        t = Thread(target=self.cost, args=(data,))
        t.start()
        if THREADBOOL:
            self.process_start()
        else:
            self.start()

    async def asyncRun(self, url):
        html = await self.html.download(url)
        data = self.parser.parser(url, html)
        self.dataout.output_mongo(data)

    @costTime
    def eventLoop(self):
        t = Thread(target=self.monitor)
        t.start()
        n = 0
        while q.qsize() != 0:
            urls = [q.get() for _ in range(DistributedNum)]
            tasks = [self.asyncRun(url) for url in urls]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
            n += 1
        t.join()

    def monitor(self):
        """
        监控进度
        :return:
        """
        all_num = 500
        end_num = self.r.get_end()

        while all_num > end_num:
            end_num = self.r.get_end()
            time.sleep(1)
            after = self.r.get_end()
            speed = after - end_num
            print('Speed: %s' % speed)
            print(end_num)


if __name__ == '__main__':
    work = Spiders()
    work.run()
