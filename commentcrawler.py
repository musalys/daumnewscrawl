# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import requests
import urlparse
import datetime
import json
from bs4 import BeautifulSoup
from newsdao_mongodb import NewsDAO
from commentdao_mongodb import CommentDAO
import multiprocessing

class CommentCrawler(object):

    '''
        crawler initialization.
    '''
    def __init__(self, newsdao, commentdao):
        self.newsdao = newsdao
        self.commentdao = commentdao
        self.recent_news = self.newsdao.get_recent_news(days=1)

    '''   < Still Working on it>

    #     get partition of urls.
    # def partition_urls(self, n):
    #     return [self.recent_news[x::n] for x in xrange(n)]


    #     start multiprocessing crawler.
    # def start_multiproc_crawlers(self, n = 5):
    #     works = []
    #     list_of_urls = self.partition_urls(n)


    #     for i in range(n):
    #         p = multiprocessing.Process(target= self.crawl_recent_news_comment, args=(list_of_urls[i],))
    #         works.append(p)
    #         p.start()


    #     call a crawl_comment method everytime that we have one link elements.
    # def crawl_recent_news_comment(self, partitioned_news):
    #     for link in partitioned_news:
    #         self.crawl_comment(link)
    '''

    '''
        now let's begin comment crawling.
    '''
    def crawl_comment(self):

        # Looping link of each article
        for link in self.recent_news:

            # get string where {} : ex) http://v.media.daum.net/v/{20161201204824265}
            m = re.search(r'v/\d+', link)
            news_id_number = m.group()[2:]

            # get comment link('http://comment.daum.net/apis/v1/posts/@news_id_number')
            origin = 'http://comment.daum.net/apis/v1/posts/@' + news_id_number
            # print origin

            # request from news posts with authorization headers and get content by using BeautifulSoup
            res = requests.get( origin, headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE0ODA2NTQ3NjEsInVzZXJfbmFtZSI6IjI2QlhBdktueTVXRjVaMDlscjVrNzdZOCIsImF1dGhvcml0aWVzIjpbIlJPTEVfVFJVU1RFRF9DTElFTlQiLCJST0xFX0NMSUVOVCJdLCJqdGkiOiI3NWYyYTNiNi1lZWVhLTRlMGItYmI5ZS1lNmQxOTVlODg3M2QiLCJjbGllbnRfaWQiOiIyNkJYQXZLbnk1V0Y1WjA5bHI1azc3WTgiLCJzY29wZSI6WyJST0xFX0NMSUVOVCJdfQ.hwBpg-FOkeXQrO2W-6FlSapa5cefGMjKAOvPsNx8rLI'})
            content = res.content
            soup = BeautifulSoup(content, 'html.parser')

            # change object type into json dictionary
            article_info = json.loads(str(soup))

            # get post_id, comment_counts and page which used in comment crawling
            post_id = article_info['id']
            comment_count = article_info['commentCount']
            page = int(comment_count/100) + 1

            # looping pages
            for i in range(page):

                # set offset unit of 100 because print limit is 100.
                offset = i * 100

                # This is genuine URL that used in comment crawling
                comment_base_url = 'http://comment.daum.net/apis/v1/posts/{}/comments?parentId=0&offset={}&limit=100&sort=RECOMMEND'.format(post_id, offset)

                # parsing with requests and bs4
                res = requests.get(comment_base_url)
                content = res.text
                soup = BeautifulSoup(content, 'html.parser')

                # jsonify for the crawling
                comments = json.loads(str(soup))

                # print '=' * 40
                # print i
                # print '=' * 40
                # print

                # if articles do not have comments return nothing
                if not comments:
                    print 'e'
                    # print ':' * 80

                # if comments exists, then crawl below informations
                for comment in comments:
                    comment_id      = comment['id']
                    news_id         = link
                    comment_content = comment['content']
                    written_time    = comment['updatedAt']
                    written_time    = datetime.datetime.strptime(written_time.split('+')[0], '%Y-%m-%dT%H:%M:%S')
                    like_count      = comment['likeCount']
                    dislike_count   = comment['dislikeCount']
                    comment_id      = news_id_number + '@' + str(post_id) + '@' + str(comment_id)

                    self.commentdao.save_comment(comment_id, news_id, str(comment_content), like_count, dislike_count, written_time)

                    # debugging
                    # print '-' * 40
                    # print comment_id
                    # print str(comment_content)
                    # print written_time
                    # print like_count
                    # print dislike_count
                    # print '-' * 40
                    # print

if __name__ == '__main__':
    newsdao = NewsDAO()
    commentdao = CommentDAO()

    crawler = CommentCrawler(newsdao, commentdao)
    crawler.crawl_comment()
    # crawler.start_multiproc_crawlers(2)
