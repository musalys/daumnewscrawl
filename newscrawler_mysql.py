# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import datetime
import requests
import json
import re
from bs4 import BeautifulSoup
#from newsdao import NewsDAO

# Crawler using Mysql


class Daum_News_Crawler(object):

    def __init__(self, newsdao, url):
        self.newsdao = newsdao
        self.url = url

    def get_topics(self):

        res = requests.get(self.url)
        content = res.content
        soup = BeautifulSoup(content)

        soup_1 = soup.find_all('a', attrs={'class': 'link_gnb'})

        topic_list_raw = []

        for soup_i in soup_1:
            topic_list_raw.append('http://media.daum.net/'+soup_i['href'][1:])
            #print soup_i['href']

        topic_lists = topic_list_raw[1:7]

        self.get_links(topic_lists)


    '''
        below is the method that crawl several news links in each topic.
    '''

    def get_links(self, urls):

        for url in urls:

            res = requests.get(url)
            content = res.content
            soup = BeautifulSoup(content)

            soup_1 = soup.find('ul', attrs={'class': 'list_news'})
            soup_2 = soup_1.find_all('a', attrs={'class': 'link_txt'})

            for k in soup_2:
                if 'http' in k['href']:
                    #print k['href']
                    link = k['href']
                    self.crawl_title_content(link)

    '''
        below is the method that crawl each article's title, content and written time.
        and save them in mysql.
    '''

    def crawl_title_content(self, link):

        res = requests.get(link)
        content = res.content
        soup = BeautifulSoup(content)

        try:
            title = soup.find('h3', attrs={'class': 'tit_view'}).get_text().strip()
            content = soup.find('div', attrs={'id': 'harmonyContainer'}).get_text().strip()
            written_time1 = soup.find('span', attrs={'class': 'info_view'}).get_text().strip()
            written_time1 = re.search(r'2\d+.\d+.\d+\s.*', written_time1)
            written_time = written_time1.group()
            #written_time2 = datetime.datetime.strptime(written_time.group().split('.'))

        except Exception as e:
            print '1', e

        try:
            print link
            print str(title)
            print written_time
            print str(content)

            #save above things in Mysql(link, title, written_time, content), links are a primary key.
            #self.newsdao.save_news(link, str(title), str(content), written_time)

        except Exception as e1:
            print '2', e1

urls = 'http://media.daum.net/'

newsdao = 'kit'
crawl = Daum_News_Crawler(urls, newsdao)

crawl.get_topics()
