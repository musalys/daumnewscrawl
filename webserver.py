# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import uuid

from flask import Flask, jsonify, request, json, Response
from newsdao_mongodb import NewsDAO
#from commentdao import CommentDAO
from memcache import MemCache

from konlpy.tag import Kkma

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def hello_world():
    return 'Hello, Welcome to YS API!'


@app.route('/test')
def hello_json():
    data = {'name' : 'Aaron', 'family' : 'Byun'}
    return jsonify(data)


@app.route('/news/search/<keyword>')
def search_news(keyword):
    newsdao = NewsDAO()
    #memcache = MemCache()

    #user_id = request.args.get('user_id')
    #apikey = request.args.get('apikey')

    # print user_id, apikey
    # if memcache.auth_user(user_id, apikey):
    #     data = newsdao.get_news_by_keyword_in_content(str(keyword))
    # else:
    #     data = {'result' : '인증에 실패하였습니다.'}
    data = newsdao.get_news_by_keyword_in_content(str(keyword))
    #return json.dumps(data, ensure_ascii=False).encode('utf8')
    return jsonify(data)


@app.route('/news/recent')
def get_recent_10():
    newsdao = NewsDAO()
    data = newsdao.get_recent_news()

    return jsonify(data)
#
# # 연습문제 1
# @app.route('/news/top5')
# def get_top_news():
#     newsdao = NewsDAO()
#     sort = request.args.get('sort')
#     top5_news = newsdao.get_top_news(sort)
#
#     return jsonify(top5_news)
#
# # 연습문제 2
# @app.route('/comment/search/<keyword>')
# def search_comment(keyword):
#     commentdao = CommentDAO()
#
#     page = int(request.args.get('page'))
#     page_size = int(request.args.get('pagesize'))
#
#     data = commentdao.get_comment_by_keyword(str(keyword), page, page_size)
#     return jsonify(data)
#
#
# # 연습문제 3
# @app.route('/news/<link>', methods = ['DELETE'])
# def delete_news(link):
#     newsdao = NewsDAO()
#     result = newsdao.delete_news(link)
#
#     return jsonify({'result' : result})
#
# # 연습문제 4
# @app.route('/auth')
# def auth():
#     memcache = MemCache()
#
#     user_id = request.args.get('user_id')
#     apikey = str(uuid.uuid4())
#
#     memcache.hold_user_key(user_id, apikey)
#     return jsonify({'apikey' : apikey})
#
# @app.route('/similar_news/<news_id>')
# def get_similar_news(news_id):
#     ids = news_id.split(':')
#     news_id = 'http://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1={}&oid={}&aid={}'.format(ids[0], ids[1], ids[2])
#
#     newsdao = NewsDAO()
#     similar = newsdao.get_similar_news(news_id)
#
#     return jsonify(similar)
#
#
# @app.route('/news/test', methods=['POST'])
# def news_post_test():
#     print request
#     test = request.form['email']
#     print request.form['password']
#
#     return jsonify({'result' : 1})
#
# @app.route('/users', methods=['GET'])
# def users():
#     user_id = request.args.get('user_id')
#     return jsonify({'user' : user_id})
#
# @app.route('/users/<int:user_id>', methods=['GET'])
# def users_rest(user_id):
#     return jsonify({'user' : user_id})
#
# @app.route('/method', methods=['GET', 'POST', 'DELETE'])
# def method():
#     if request.method == 'GET':
#         print request.args.get('user')
#         print 'GET'
#     elif request.method == 'POST':
#         print 'POST'
#     elif request.method == 'DELETE':
#         print 'DELETE'
#     elif request.method == 'PUT':
#         print 'PUT'
#
#     return jsonify({'result' : request.method})

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
