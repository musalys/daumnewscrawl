# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import datetime
import requests
import json
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient


#아마존 웹서버의 몽고 DB의 news db에 연결

server = 'ec2-35-164-25-57.us-west-2.compute.amazonaws.com'
mongo = MongoClient(server, 27017)
news = mongo.daum.news


class NewsDAO(object):

    def __init__(self):
        pass

    def save_news(self, link, title, content, written_time, crawl_time=datetime.datetime.now()):

        news.update_one({'link' : link}, {'$set' : {'title' : title, 'content' : content, 'written_time' : written_time, 'crawl_time': crawl_time}}, upsert=True)

    def get_recent_news_by_id(self, link):
        pass
