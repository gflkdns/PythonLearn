import datetime
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import re


def draw(keys, values):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    time = i = datetime.datetime.now()
    plt.title(str(time.year) + "/" + str(time.month) + "/" + str(time.day) + zhiwei + "职位数分布图")
    plt.bar(keys, values, label="职位数")
    plt.legend()
    plt.show()


def getCitys(citys):
    urlPath = "http://www.zhaopin.com/citymap.html"
    print("开始爬取：")
    r = requests.get(urlPath)
    if r.ok:
        r.raise_for_status()
        r.encoding = 'utf-8'
        data = r.text
        print("目标url：", urlPath)
        soup = BeautifulSoup(data, 'html.parser')
        a = soup.find_all('strong')
        for i in a:
            try:
                citys.append(i.contents[0])
            except:
                continue
    else:
        print("城市获取失败！")


def getData(citys, data):
    for city in citys:
        headers = {
            'Host': 'blog.csdn.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://www.baidu.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
        }
        zhilianUrl = "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=" + city + "&kw=" + zhiwei + "&p=1&isadv=0"
        r = requests.get(zhilianUrl, headers=headers)
        if r.ok:
            r.raise_for_status()
            r.encoding = 'utf-8'
            rr = r'(?!共<em>)[0-9]+(?=</em>个职位满足条件)'
            a = re.findall(rr, r.text, 0)

            if int(a[0]) >= 50 and hasCity(r):
                print(city, zhiwei, a[0])
                data[city] = int(a[0])
        else:
            print("城市获取失败！")

def hasCity(r):
    soup = BeautifulSoup(r.text, 'html.parser')
    loc = soup.find_all('input')
    for i in loc:
        try:
            href = i.attrs['id']
            if href == "JobLocation":
                if i.attrs['value'] == "全国":
                    return False
        except:
            continue
    return True


zhiwei = "android"
if __name__ == '__main__':
    citys = []
    data = {
        # "qq": 123,
        # "q1q": 123,
        # "qq2": 123,
    }
    # 获得所有的城市
    getCitys(citys)
    print("结果", citys)

    getData(citys, data)
    print(data)
    data2 = sorted(data.items(), key=lambda d: d[1], reverse=True)
    print(data2)
    result = {}
    for x in range(10,26):
        print(data2[x])
        result[data2[x][0]] = data2[x][1]
    draw(result.keys(), result.values())
