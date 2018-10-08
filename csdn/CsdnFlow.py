import re
import requests
from bs4 import BeautifulSoup

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
              'UserName=qq_27512671;'
              ' UserInfo=516ZoXsRpXNZVFVGH2xffreDWYzmqhRd%2FPjQLP5E3cgKhwAZP2g0j2UUVMxpPV8YnDf1vvRCE7AKkIQNrB4xWyZQ8LqmbWFWcTZCEE0nt%2B1SjCJ0UTXxgeN0oAHvPF4ZXDtdRiwBUP4Yq%2BDpKVXibA%3D%3D;'
              ' UserNick=%E7%97%95%E8%BF%B9%E4%B8%B6;'
              ' AU=31E; BT=1533529462474; '
              'UserToken=516ZoXsRpXNZVFVGH2xffreDWYzmqhRd%2FPjQLP5E3cgKhwAZP2g0j2UUVMxpPV8YnDf1vvRCE7'
              'AKkIQNrB4xWyZQ8LqmbWFWcTZCEE0nt%2B1SjCJ0UTXxgeN0oAHvPF4Z%2F%2Fg9Qg%2Bu1QGldHvsTz5dbi2xCE'
              'Cl9rSvzPnwp1K%2Fi6zs3BXOd7V7mf74RyRZ5agg; dc_tos=pd0ux1; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1533529477'
}


def follow(username):
    follow = "https://my.csdn.net/index.php/follow/do_follow?" \
             "username={username}" \
             "&jsonpcallback=jQuery190003126168270004337_1533532739748" \
             "&_=1533532739752".format(username=username)
    try:
        r = requests.get(follow, headers=headers, verify=False, )
    except:
        pass
    print("follow:", username,
          "status_code:", r.status_code,
          "message:", r.content

          )


followedUsers = []


def getUserId(user):
    url = 'https://my.csdn.net/{userid}'.format(userid=user)
    print("开始爬取：")
    try:
        r = requests.get(url, headers=headers)
        if r.ok:
            r.raise_for_status()
            r.encoding = 'utf-8'
            rr = "username='[^<>]*'"
            a = re.findall(rr, r.text, 0)
            for i in a:
                i = i[10:-1]
                # 不为空并且没有关注过
                if i != '' and i not in followedUsers:
                    # 关注
                    follow(i)
                    # 放入已经关注列表
                    followedUsers.append(i)

        else:
            print("用户获取失败！", r.status_code)
    except:
        pass



def unFollow(username):
    url = "https://my.csdn.net/index.php/my/follow/do_unfollow"
    try:
        r = requests.post(url, data={
            "username": username
        }, headers=headers, verify=False, )
        if r.ok:
            print("un follow:", username)
        else:
            print("un follow ", username, " error")
    except:
        pass



def getFollowMyUser():
    for i in range(50):

        url = 'https://my.csdn.net/my/follow/{page}'.format(page=i)
        try:
            r = requests.get(url, headers=headers, verify=False)
        except:
            pass
        r.raise_for_status()
        r.encoding = 'utf-8'
        data = r.text
        soup = BeautifulSoup(data, 'html.parser')
        a = soup.find_all('a')
        for al in a:
            if "class" in dict(al.attrs):
                clas = al.attrs["class"]
                if clas[0] == 'user_name':
                    unFollow(al.contents[0])


if __name__ == '__main__':
    getFollowMyUser()
    getUserId('flysky_jay')
    for i in followedUsers:
        # 迭代
        getUserId(i)
