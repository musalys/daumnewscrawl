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
import multiprocessing

# connect to aws ec2 mongo db server

server = 'ec2-35-164-25-57.us-west-2.compute.amazonaws.com'
mongo = MongoClient(server, 27017)
news = mongo.daum.news
comment = mongo.daum.comments


class CommentDAO(object):

    def __init__(self):
        pass

    def save_comment(self, comment_id, news_id, comment_content, like_count, dislike_count,  written_time, crawl_time = datetime.datetime.now()):
        # saved = False

        # save comment if it doesn't exists
        if not self.get_comment_by_id(comment_id):
            print comment_id, 's'
            comment.insert_one({'comment_id': comment_id,
                                'news_id': news_id,
                                'comment_content': comment_content,
                                'like_count': like_count,
                                'dislike_count': dislike_count,
                                'written_time': written_time,
                                'crawl_time': crawl_time})
            # saved = True
            # return saved

    def get_comment_by_id(self, comment_id):

        # search comment by comment id
        result = comment.find({'comment_id': comment_id})

        if result.count() > 0:
            return True

        return False
        # except NoResultFound as e:
        #     print e
        #     return False
        # except MultipleResultsFound as e:
        #     print e
        #     return True
