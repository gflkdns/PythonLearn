import re
import requests
import urllib.parse
from bs4 import BeautifulSoup

headers = {
    'Host': 'www.qichacha.com',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://www.qichacha.com/search?key=%E5%8C%97%E4%BA%AC%E5%8D%8E%E5%A4%8F%E6%B0%B8%E4%B9%90',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'UM_distinctid=1661a64e917240-0afcd552852336-454c092b-100200-1661a64e9182bc; zg_did=%7B%22did%22%3A%20%221661a64e9922d0-06b75f26f6072-454c092b-100200-1661a64e99342e%22%7D; _uab_collina=153804111307470208251594; saveFpTip=true; acw_tc=7cc1e21815502295621214264ef2e3eca7a3b105ef9ab56c95d2205cc5; hasShow=1; QCCSESSID=5lvcjoi61id08fn9i63lh82u95; CNZZDATA1254842228=176235367-1538039823-https%253A%252F%252Fwww.baidu.com%252F%7C1552269633; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1551424764,1551856127,1552267975,1552269912; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201552269911390%2C%22updated%22%3A%201552272633709%2C%22info%22%3A%201551856120273%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%2C%22cuid%22%3A%20%227bd0ac05d873ace4e899d1ecd1a60f43%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1552272634',}

# 获取分支机构
def get_branches(company_name):
    url="https://www.qichacha.com/search?key={company_name}".format(company_name=company_name)
    r = requests.get(url,headers=headers,verify=False)
    if r.ok:
        r.raise_for_status()
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml')
        fr=soup.find_all(class_='m-t-xs')
        print(fr)
        for a in fr:
            print(a)

    else:
        print("用户获取失败！", r.status_code)

if __name__ == '__main__':
    get_branches("北京华夏永乐科技有限公司")