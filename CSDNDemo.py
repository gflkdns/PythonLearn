import requests
from bs4 import BeautifulSoup


def data(url):
    r = requests.get(url)
    if r.ok:
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    else:
        return ""


if __name__ == '__main__':
    data = data("http://blog.csdn.net/qq_27512671?viewmode=contents")
    soup = BeautifulSoup(data, 'html.parser')
    a = soup.find_all('a')
    lst = set()
    for i in a:
        try:
            href = i.attrs['href']
            if "qq_27512671/article/details" in href and not "comments" in href:
                lst.add(href)
        except:
            continue
    print(str(lst.__len__()) , lst)
    while True:
        for i in lst:
            try:
                url = "http://blog.csdn.net" + i
                re = requests.get(url)
                if re.ok:
                    print("success:" + url)
                else:
                    print("error:" + url)
            except:
                continue
