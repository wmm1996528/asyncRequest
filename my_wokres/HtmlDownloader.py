import requests
from my_wokres import RedisWorker
import time
from setting import *
import aiohttp


class HtmlDownloader(object):
    def __init__(self, proxy_bool=None):
        self.proxy = None
        self.bool = proxy_bool

    @staticmethod
    def _get_ip():
        url = 'http://127.0.0.1:5555/ip'
        ip = requests.get(url).text
        proxy = {
            'http': ip,
            'https': ip,
        }
        return proxy

    async def download(self, url):
        if self.bool:
            self.proxy = self._get_ip()
        else:
            pass
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
