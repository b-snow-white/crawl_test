# -*- coding: utf-8 -*-
"""
@time:2018/7/12 20:13

@author: BX
"""

from urllib.parse import  urlencode
import requests
from pyquery import PyQuery as pq
from pymongo import MongoClient
base_url='https://m.weibo.cn/api/container/getIndex?'
headers={
    'host':'m.weibo.cn',
    'Referer':'https://m.weibo.cn/u/2830678474',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) ' \
                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'
}
def get_page(page):
    params={'type':'uid',
            'value':'2830678474',
            'containerid':'1076032830678474',
            'page':page}
    url=base_url+urlencode(params)#urlencode将参数转换为url的GET请求参数
    try:
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error:',e.args)
def parse_page(json):
    if json:
        items=json.get('data').get('cards')
        for item in items:
            item=item.get('mblog')
            weibo={}
            weibo['id']=item.get('id')
            weibo['text']=pq(item.get('text')).text()
            weibo['attritudes']=item.get('comments_count')
            weibo['reposts']=item.get('reposts_count')
            weibo['date']=item.get('created_at')
            yield weibo
client=MongoClient()
db=client['weibo']
collection=db['test']
def save_to_mongodb(result):
    if collection.insert(result):
        print('Save to mongodb')
if __name__=='__main__':
    for page in range(2,10):
        json=get_page(page)
        #print(json)
        results=parse_page(json)
        for result in results:
            print(result)
            save_to_mongodb(result)

