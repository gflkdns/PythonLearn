#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


def getComList(html, lst):
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('p')
    for i in a:
        try:
            href = i.attrs['class']
            if href[0] == "":
                lst.append(i.contents[0])
        except:
            continue


com = []
page = 0
while True:
    urlPath = "https://movie.douban.com/subject/27024903/comments?start=" + str(
        page) + "&limit=20&sort=new_score&status=P"
    print("开始爬取：")
    r = requests.get(urlPath)
    if r.ok:
        r.raise_for_status()
        r.encoding = 'utf-8'
        data = r.text
        print("目标url：", urlPath)
        getComList(data, com)
        page += 20
    else:
        break

print("爬取结果(" + str(com.__len__()) + ")：-------↓--------",)
for i in com:
    print('评论：', i)
