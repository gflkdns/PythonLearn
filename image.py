import os
import re
import urllib
import uuid

import requests
from bs4 import BeautifulSoup
from requests import request

urlPath = 'http://www.quanjing.com/'
localPath = 'd:\\pythonPath'


def gethemltext(url):
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r.text


def getImageList(html, lst):
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('img')
    for i in a:
        try:
            href = i.attrs['src']
            lst.append(href)
        except:
            continue


def start():
    root = "http://www.quanjing.com/"
    html = gethemltext("http://www.quanjing.com/?audience=151316")
    list = []
    getImageList(html, list)
    tmp = 0
    for src in list:
        try:
            print(root + src)
            urllib.request.urlretrieve(root + src, r'D:\pythonPath\%s.jpg' % tmp)
            tmp = tmp + 1
            print('成功')
        except:
            print('失败')
    print('下载完毕')
#开始获取
start()
