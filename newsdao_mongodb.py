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

server = 'ec2-35-164-25-57.us-west-2.compute.amazonaws.com'
mongo = MongoClient(server, 27017)
news = mongo.daum.news


class NewsDAO(object):

    def __init__(self):
        pass

    def save_news(self, link, title, content, written_time, crawl_time=datetime.datetime.now()):
        saved = False
        # check if the article's link is in mongo DB's collections
        if not self.get_news_by_id(link):
            news.insert_one({'link': link, 'title': title, 'content': content, 'written_time': written_time, 'crawl_time': crawl_time})
            saved = True
            # news.update_one({'link': link}, {'$set': {'title': title, 'content': content, 'written_time': written_time, 'crawl_time': crawl_time}}, upsert=True)
        return saved

    def get_news_by_id(self, link):

        result = news.find({'link': link})

        if result.count() > 0:
            return True

        return False

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
            # articles['written_time'] = doc['written_time']
            #articles['crawl_time'] = datetime.datetime.strftime(doc['crawl_time'], "%Y-%m-%d %H:%M:%S")

            data.append(articles)

        # print data
        return data

    def get_recent_news(self, days=2):

        '''
            db.news.aggregate([
                    { $project: { link: '$link', dateDifference: { $subtract: [ new Date(), "$written_time" ] } } },
                    { $match: { dateDifference : { $lte: 1000 * 60 * 60 * 24 * days } } }
                ])
        '''

        now = datetime.datetime.now()

        pipelines=[]
        pipelines.append({'$project': {'link': '$link', 'title': '$title', 'content': '$content', 'written_time': '$written_time', 'crawl_time': '$crawl_time', 'dateDifference': {'$subtract' : [ now, '$written_time']}}})
        pipelines.append({'$match': {'dateDifference': {'$lte': 1000 * 60 * 60 * 24 * days }}})
        pipelines.append({'$sort': {'dateDifference': 1}})
        # pipelines.append({'$limit': 10})

        result = news.aggregate(pipelines)

        data = []

        for doc in result:
            # articles = {}
            # articles['link'] = doc['link']
            # articles['title'] = doc['title']
            # articles['content'] = doc['content']
            # articles['written_time'] = doc['written_time']
            # articles['crawl_time'] = doc['crawl_time']
            data.append(doc['link'])

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
