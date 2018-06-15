import requests
from my_wokres import RedisWorker
import time
from setting import *
import aiohttp


class HtmlDownloader(object):
    def __init__(self, proxy_bool=None):
        self.bool = proxy_bool

    def _get_ip(self):
        url = 'http://127.0.0.1:5555/ip'
        ip = requests.get(url).text
        proxy = {
            'http': ip,
            'https': ip,
        }
        return proxy

    async def download(self, url):
        if self.bool == True:
            self.proxy = self._get_ip()
        else:
            self.proxy = None
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
