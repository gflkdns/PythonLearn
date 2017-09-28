import os
import urllib

import requests
from bs4 import BeautifulSoup

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
            href = i.attrs['data-original']
            lst.append(href)
        except:
            continue


def main():
    html = gethemltext("https://www.douyu.com/directory/game/yz")
    list = []
    getImageList(html, list)
    dir = "D:\pythonPath\\"
    if not os.path.exists(dir):
        os.makedirs(dir)
    tmp = 0
    for src in list:
        try:
            print(src)
            urllib.request.urlretrieve(src, dir + '%s.jpg' % tmp)
            tmp += 1
            print('success')
        except:
            print('error')
    print('finished')


# start get image
main()
