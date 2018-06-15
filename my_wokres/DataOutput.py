from pymongo import MongoClient

from setting import *


class DataOutput(object):
    def __init__(self):
        self.conn = MongoClient(MONGO_URL, connect=False)
        self.coll = self.conn.guazi
        self.db = self.coll.cars

    def output_mongo(self, data):
        try:
            self.db.insert(data)
        except Exception as e:
            logger.warning(data)
            logger.warning(e)
