# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import re
from bs4 import BeautifulSoup
#from newsdao import NewsDAO

class Daum_News_Crawler(object):

    def __init__(self, newsdao, url):
        self.newsdao = newsdao
        self.url = url


    def get_topic_links(self):

        res = requests.get(self.url)
        content = res.content
        soup = BeautifulSoup(content)

        soup_1 = soup.find_all('li')

        for i in range(4,10):
            try:
                if 'link_gnb' in soup_1[i].a['class']:
                    topic_urls = self.url + soup_1[i].a['href'][1:]
                    self.get_links(topic_urls)
            except Exception as e:
                print 'e'


    def get_links(self, urls):

        res = requests.get(urls)
        content = res.content
        soup = BeautifulSoup(content)

        try:
            soup_1 = soup.find('ul', attrs = {'class' : 'list_news'})
            soup_2 = soup_1.find_all('a', attrs = {'class' : 'link_txt'})

            for k in soup_2:
                if 'http' in k['href']:
                    #print k['href']
                    link = k['href']
                    #print link
                    self.crawl_title_content(link)

        except Exception as e:
            print 'e1'


    def crawl_title_content(self, link):

        res = requests.get(link)
        content = res.content
        soup = BeautifulSoup(content)

        try:

            title = soup.find('h3', attrs = {'class' : 'tit_view'}).get_text().strip()
            #title = re.sub(r'^[*]', '', title)
            content = soup.find('div', attrs = {'id' : 'harmonyContainer'}).get_text().strip()
            #content = re.sub(r'^\[*\]', '', content)
            written_time = soup.find('span', attrs = {'class' : 'txt_info'}).get_text().strip()
            #written_time = re.sub(r'^...', '', written_time)

        except Exception as e:
            print 'e2'

        print link
        print title
        print written_time
        #self.newsdao.save_news(link, title, content, written_time)

        #print title
        #print
        #print written_time
        #print
        #print content
        #print


url = 'http://media.daum.net/'
newsdao = 'kit'#NewsDAO()
#link1 = 'http://v.media.daum.net/v/20161022094104633'

crawler = Daum_News_Crawler(newsdao, url)
crawler.get_topic_links()
