#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser
import base64
import json
import hashlib
import random
import time
import sys
import io
import cgi
import os
import requests

from spider import hawkeye_conf, get_conf, md5, send_mail

from email.mime.text import MIMEText
from email.header import Header
from pymongo import MongoClient
from utils import leakage_col, query_col, blacklist_col, notice_col

def getjsonobj(resp):
    """
    get json object from an HTTP response
    """
    return json.loads(resp.text.encode(resp.encoding).decode('utf-8'))

def crawl(query):
    search_url = 'https://api.github.com/search/code?q={}&type=Code&utf8=%E2%9C%93'
    token = get_conf('GitHub', 'APITOKEN')
    
    search_resp = requests.get(search_url.format(query['keyword']), headers = {'Authorization': 'token '+token})

    if get_conf('GitHub', 'APIERROR') in search_resp.text:
        print('登录失败')
        exit(0)

    #parse json
    search_json = getjsonobj(search_resp)
    print("total_count",search_json['total_count'])
    if search_json['total_count'] <= 0:
        pass
    for item in search_json['items']:
        try:
            in_blacklist = False
            leakage = {}
            
            leakage['datetime'] = None
            leakage['link'] = item['html_url']
            leakage['project'] = item['repository']['full_name']
            leakage['_id'] = md5(leakage['link'])
            for blacklist in blacklist_col.find({}):
                print(blacklist['keyword'])
                print('\n' in blacklist['keyword'])
                if blacklist['keyword'].lower() in leakage['link'].lower():
                    in_blacklist = True
                    break
            if in_blacklist:
                continue
            if leakage_col.find_one({"project": leakage['project'], "ignore": 1}):
                continue
            if leakage_col.find_one({"link": leakage['link'], "datetime": leakage['datetime']}):
                continue
            if leakage_col.find_one({'_id': leakage['_id']}):
                continue

            item_url_resp = requests.get(item['url'])
            item_url_json = getjsonobj(item_url_resp)
            #get source code
            code_resp = requests.get(item_url_json['download_url']) 
            code = code_resp.text.encode(
                code_resp.encoding).decode('utf-8')
            leakage['code'] = base64.b64encode(
                code.encode(encoding='utf-8')).decode()
            #leakage['code'] = item_url_json['content']
            leakage['username'] = item['repository']['owner']['login']
            leakage['language'] = None
            # file path start from username followed with repo's name
            fullurl = item_url_json['url']
            urlinfo = fullurl.split(r'https://api.github.com/repos/')[1]
            urlinfo = urlinfo.split('?')[0]
            leakage['filename'] = urlinfo
            leakage['tag'] = query['tag']
            # can't fetch code segment details in
            leakage['detail'] = None
            leakage['security'] = 0
            leakage['ignore'] = 0

            #save to mongoDB
            leakage_col.save(leakage)

            #sleep to anti blocked by the site
            minsecs = int(get_conf('AntiBlock', 'MIN_SLEEP_SECONDS'))
            maxsecs = int(get_conf('AntiBlock', 'MAX_SLEEP_SECONDS'))
            time.sleep(random.randint(minsecs, maxsecs))

            try:
                if int(get_conf('Notice', 'ENABLE')):
                        email_content = '''
                            <h3>命中规则:</h3> 
                            <span>{}</span>
                             <br>
                            <h3>文件地址:</h3>
                            <span>{}</span>
                            <br>
                            <h3>代码:</h3>
                            <pre><code style="background-color: #f6f8fa;white-space: pre;">{}</code></pre>
                            '''.format(
                            leakage['tag'], leakage['link'], cgi.escape(code))
                        send_mail(email_content)
                else:
                    pass

            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
    #if 'next_page disabled' in resp.text:
    #        break

if __name__ == "__main__":
    for query in query_col.find()[::]:
        print(query['tag'])
        crawl(query)
