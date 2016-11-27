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


# connect to aws ec2 mongo db server

server = 'server'
mongo = MongoClient(server, 27017)
news = mongo.daum.news


class NewsDAO(object):

    def __init__(self):
        pass

    def save_news(self, link, title, content, written_time, crawl_time=datetime.datetime.now()):

        # if the article's link is in mongo DB's collections
        news.update_one({'link': link}, {'$set': {'title': title, 'content': content, 'written_time': written_time, 'crawl_time': crawl_time}}, upsert=True)

    def get_news_by_id(self, link):
        pass

    def get_news_by_keyword_in_content(self, keyword):

        '''
            db.news.aggregate([ {$match : { $text: {$search : "keyword"}}}])
        '''
        news.create_index([('content', 'text')])
        pipelines = []
        pipelines.append({"$match": {"$text": {"$search": keyword}}})
        result = news.aggregate(pipelines)

        data = []

        for doc in result:
            articles = {}
            articles['title'] = doc['title']
            articles['link'] = doc['link']
            articles['content'] = doc['content']
            articles['written_time'] = doc['written_time']
            #articles['crawl_time'] = datetime.datetime.strftime(doc['crawl_time'], "%Y-%m-%d %H:%M:%S")

            data.append(articles)

        # print data
        return data

# '''
#     db.news.aggregate([ {$match : { $text: {$search : "keyword"}}}])
# '''
# news.create_index([('content','text')])
# pipelines=[]
# pipelines.append({"$match" : {"$text": {"$search": "아이폰"}}})
# result = news.aggregate(pipelines)
#
# data = []
#
# for doc in result:
#     data.append(doc)
#
# print len(data), data
# return data
