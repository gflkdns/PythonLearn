import re
import requests
import urllib.parse
from bs4 import BeautifulSoup

from csdn.CsdnFlow import follow, unFollow

headers = {
    'Host': 'my.csdn.net',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'https://blog.csdn.net/zwj1452267376/article/details/49359983',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'uuid_tt_dd=10_20345892100-1524212903385-435733;'
              ' Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=1788*1*PC_VC; '
              'kd_user_id=7295273f-7b6b-4192-b9a7-c942e97d0b84;'
              ' UN=qq_27512671;'
              ' UM_distinctid=163876d887ba03-0aaf3090c6e7a3-44410a2e-100200-163876d887c9e9;'
              ' smidV2=20180703093604202daee73a21697260c8c4497935dbeb0080764ec19be9550;'
              ' __utma=17226283.374765269.1526985204.1528946860.1530611441.4; '
              '__utmz=17226283.1530611441.4.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic;'
              ' dc_session_id=10_1533528901844.947334;'
              ' Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1533526931,1533527162,1533528902,1533529447; '
              'UserName=qq_275546671;'
              ' UserInfo=516ZoXsRpd%2FPjQLP5E3cgKhwAZP2g0j2UUVMxpPV8YnDf1vvRCE7AKkIQNrB4xWyZQ8LqmbWFWcTZCEE0nt%2B1SjCJ0UTXxgeN0oAHvPF4ZXDtdRiwBUP4Yq%2BDpKVXibA%3D%3D;'
              ' UserNick=%E7%97%9%B9%E4%B8%B6;'
              ' AU=31E; BT=1533529462474; '
              'UserToken=516ZoXs2xffreDWYzmqhRd%2FPjQLP5E3cgK'
              'hwAZP2g0j2UUVMxpPV8YnDf1vvRCE7AKkIQNrB4xWyZQ8LqmbWFWcTZCEE0nt%2B1SjCJ0UTXxgeN0oAHvPF4Z%'
              '2F%2Fg9Qg%2Bu1QGldHvsTz5dbi2xCECl9rSvzPnwp1K%2Fi6zs3BXOd7V7mf74RyRZ5agg'
}

followedUsers = []


def sendMesage(userid, message):
    url = "http://msg.csdn.net/letters/send_message" \
          "?receiver={userid}" \
          "&body={message}" \
        .format(userid=userid, message=urllib.parse.quote(message))
    print("发消息：receiver={userid}&body={message}".format(userid=userid, message=urllib.parse.quote(message)))
    try:
        r = requests.get(url, headers=headers, verify=False)
    except:
        pass
    if r.ok:
        r.raise_for_status()
        r.encoding = 'utf-8'
        print("发消息成功：receiver={userid}&body={message}".format(userid=userid, message=message))
    else:
        print("发消息失败：receiver={userid}&body={message}".format(userid=userid, message=message))


def getUserId(user):
    url = 'https://my.csdn.net/{userid}'.format(userid=user)
    print("开始爬取：")
    r = requests.get(url, headers=headers, verify=False)
    if r.ok:
        r.raise_for_status()
        r.encoding = 'utf-8'
        rr = "username='[^<>]*'"
        a = re.findall(rr, r.text, 0)
        for i in a:
            i = i[10:-1]
            # 不为空并且没有关注过
            if i != '' and i not in followedUsers:
                print('------------------------------------------------')
                # 发消息
                sendMesage(i, "hello,我是一只虫")
                # 关注
                follow(i)
                # 取消关注
                unFollow(i)
                # 放入已发消息列表
                followedUsers.append(i)
                print('------------------------------------------------')

    else:
        print("用户获取失败！", r.status_code)


if __name__ == '__main__':
    # 。。母体。。
    getUserId('chenbang110')
    for i in followedUsers:
        # 迭代
        getUserId(i)
