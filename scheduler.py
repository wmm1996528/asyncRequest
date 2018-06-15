import my_wokres.RedisWorker
from my_wokres.HtmlDownloader import HtmlDownloader
from my_wokres.HtmlParser import HtmlParser
from my_wokres.DataOutput import DataOutput
from multiprocessing import Process
from setting import *
import time
import sys
import asyncio


def costTime(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        func(*args, **kwargs)
        t2 = time.time()
        print(t2 - t1)

    return wrapper


sys.path.append("..")


class Spiders():
    def __init__(self):
        self.r = my_wokres.RedisWorker.redisQueue('new')
        self.html = HtmlDownloader(None)
        self.parser = HtmlParser()
        self.dataout = DataOutput()
        self.r.put(URLS)

    def start(self):
        while self.r.get_size() != 0:
            url = self.r.get_wait()

            html = self.html.download(url)
            data = self.parser.parser(url, html)
            self.dataout.output_mongo(data)

    def process_start(self):
        process = []
        for i in range(THREADNUM):
            p = Process(target=self.start, args=())
            process.append(p)
        for i in range(THREADNUM):
            logger.info('Process %s running........' % i)
            process[i].start()
        for i in range(THREADNUM):
            process[i].join()
            logger.info('Process %s completed........' % i)

    @costTime
    def run(self):
        if THREADBOOL:
            self.process_start()
        else:
            self.start()

    async def asyncrun(self, url):
        html = await self.html.download(url)
        data = self.parser.parser(url, html)
        print(data)
        self.dataout.output_mongo(data)

    @costTime
    def eventLoop(self):
        urls = [i.decode() for i in self.r.get_all()]
        tasks = [self.asyncrun(url) for url in urls]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))


spider = Spiders()
if __name__ == '__main__':
    work = Spiders()
    work.eventLoop()

    # def sua():
    #     n = 0
    #     for i in range(1000):
    #         n += i
    #
    #
    # sua()
