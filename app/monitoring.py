from flask import Flask, render_template, request
from pymongo import MongoClient
from my_wokres import RedisWorker
import logging
import time
import json

app = Flask(__name__)
conn = MongoClient('mongodb://127.0.0.1:27017')
coll = conn.guazi
db = coll.cars

redisdb = RedisWorker.redisQueue('new')
from flask.logging import default_handler
app.logger.level = logging.ERROR
logger = logging.getLogger("mylog")
fmter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
hdlr = logging.FileHandler("pro.log")
hdlr.setFormatter(fmt=fmter)
app.logger.addHandler(hdlr=hdlr)
@app.route('/')
def index():

    return 'This is Spider web!'




@app.route('/speed')
def speed():
    data = redisdb.get_monit()
    return data


@app.route('/result')
def result():
    args = request.args
    limit = int(args.get('limit'))
    offset = int(args.get('offset'))
    datalength = db.find({}).count()
    data = list(db.find({}).limit(limit).skip(offset))
    data_name = list(data[1].keys())
    # print(data_name[1])
    return render_template('result.html', datas=data, data_name=data_name, len=datalength, limit=limit)


@app.route('/status')
def status():
    allUrl = redisdb.get_size()
    endUrl = redisdb.get_old()
    progess = str(round((endUrl / allUrl) * 100, 3))
    datas = [progess, allUrl, endUrl, allUrl - endUrl, '1', '2']
    return render_template('status.html', datas=datas)


if __name__ == '__main__':
    app.run(port=2121)
