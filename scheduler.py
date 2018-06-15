import my_wokres.RedisWorker
from my_wokres.HtmlDownloader import HtmlDownloader
from my_wokres.HtmlParser import HtmlParser
from my_wokres.DataOutput import DataOutput
from multiprocessing import Process
from setting import *
import time
import sys
import asyncio
import queue

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
        self.html = HtmlDownloader(None)
        self.parser = HtmlParser()
        self.dataout = DataOutput()
        # self.r.put(URLS)

    def start(self):
        while self.r.get_size() != 0:
            url = self.r.get_wait()

            html = self.html.download(url)
            data = self.parser.parser(url, html)
            self.dataout.output_mongo(data)

    def process_start(self):
        process = []
        for thread in range(THREADNUM):
            p = Process(target=self.start, args=())
            process.append(p)
        for thread in range(THREADNUM):
            logger.info('Process %s running........' % thread)
            process[thread].start()
        for thread in range(THREADNUM):
            process[thread].join()
            logger.info('Process %s completed........' % thread)

    @costTime
    def run(self):
        if THREADBOOL:
            self.process_start()
        else:
            self.start()

    async def asyncRun(self, url):
        html = await self.html.download(url)
        data = self.parser.parser(url, html)
        print(data)
        self.dataout.output_mongo(data)

    @costTime
    def eventLoop(self):
        n = 0
        while q.qsize() != 0:
            print('di %s ci' % n)
            urls = [q.get() for _ in range(DistributedNum)]
            tasks = [self.asyncRun(url) for url in urls]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
            n += 1
            print('%s jieshu'  % n)
            time.sleep(10)

spider = Spiders()
if __name__ == '__main__':
    work = Spiders()
    work.eventLoop()
