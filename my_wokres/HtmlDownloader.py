import requests
from my_wokres import RedisWorker
import time
from setting import *
import aiohttp

requests.packages.urllib3.disable_warnings()


class HtmlDownloader(object):
    def __init__(self):
        self.proxy = None
        self.bool = PROXYIP
        self.session = requests.session()
        # if self.bool is True:
        #     get_ip()

    async def download(self, url):
        if url is None:
            return None

        while True:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=HEADERS, proxy=self.proxy) as res:
                    if res.status == 200:
                        RedisWorker.redisdb.put_old(url)
                        return await res.text()
                    else:
                        logger.warning(res.status)

                    time.sleep(0.5)

    def downnload_not_wait(self, url):
        global proxies
        print(proxies)
        if url is None:
            return None
        while True:
            try:
                res = requests.get(url.decode(), headers=HEADERS, proxies=proxies, timeout=10, verify=False)
                RedisWorker.redisdb.put_old(url)
                return res.text
            except Exception as e:
                print(e)
                proxies = get_ip()
