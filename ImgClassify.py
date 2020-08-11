# !/usr/bin/python
# -*- coding:utf8 -*-
import getopt
import time
import shutil, os
import sys
import exifread
import requests
import json

in_path = ''
out_path = ''


def getLocation(GPSLatitude, GPSLongitude):
    # http://api.map.baidu.com/reverse_geocoding/v3/?
    # ak=6oq2afS16woFO4VHB4xmHXGUvyRFrY9G
    # &output=json
    # &coordtype=wgs84ll
    # &location=31.225696563611,121.49884033194
    if GPSLongitude == '' or GPSLatitude == '':
        return ''

    du = GPSLatitude.values[0].num  # 度
    fen = GPSLatitude.values[1].num  # 分
    miao = GPSLatitude.values[2].num / GPSLatitude.values[2].den  # 秒
    latitude = (miao / 60.0 + fen) / 60.0 + du

    du = GPSLongitude.values[0].num  # 度
    fen = GPSLongitude.values[1].num  # 分
    miao = GPSLongitude.values[2].num / GPSLongitude.values[2].den  # 秒
    longitude = (miao / 60.0 + fen) / 60.0 + du

    result = requests.get(url="http://api.map.baidu.com/reverse_geocoding/v3/", params={
        'ak': '6oq2afS16woFO4VHB4xmHXGUvyRFrY9G',
        'output': 'json',
        'coordtype': 'wgs84ll',
        'location': '{latitude},{longitude}'.format(latitude=latitude, longitude=longitude),
    })
    if result.status_code == 200:
        jsonText = json.loads(result.text)
        statusStr = jsonText.get('status', "")
        if statusStr == 0:
            comp = jsonText.get('result', {}).get('addressComponent', {})
            city = comp.get('city')
            district = comp.get('district')
            street = comp.get('street')
            return city + "/" + district  # + "/" + street
    return ''


def getTimeAndDesc(filePath):
    f = open(filePath, 'rb')
    tags = exifread.process_file(f)
    GPSLatitude = tags.get('GPS GPSLatitude', '')
    GPSLongitude = tags.get('GPS GPSLongitude', '')
    make = tags.get('Image Make', '')
    model = tags.get('Image Model', '')
    time = os.path.getmtime(filePath)

    location = getLocation(GPSLatitude, GPSLongitude)

    if location == '':
        if make != "" and model != "":
            devName = make + "-" + model
            return devName, format_time(time)
        else:
            return 'other', format_time(time)
    else:
        return location, format_time(time)


def format_time(timestamp):
    time_struct = time.localtime(timestamp)
    # return time.strftime('%Y-%m-%d %H:%M:%S', time_struct)
    return time.strftime('%Y-%m-%d', time_struct)


def find_all_file(fileList, path):
    files = os.listdir(path)
    for f in files:
        abpath = path + '/' + f
        if (os.path.isdir(abpath)):
            find_all_file(fileList, abpath)
        if (os.path.isfile(abpath)):
            fileList.append(abpath)


def main():
    fileList = []

    find_all_file(fileList, in_path)
    print(fileList)

    print("开始移动" + in_path)
    for img, i in zip(fileList, range(len(fileList))):
        tag, time = getTimeAndDesc(img)

        if (img.endswith('mp4')):
            tag = '视频'
        timepath = out_path + '/' + tag + "/" + time
        if not os.path.exists(timepath) or not os.path.isdir(timepath):
            # 新建文件夹
            os.makedirs(timepath, mode=0o777, exist_ok=True)

        # 将这个文件移动到timedir
        print(i + 1, "/", fileList.__len__(), tag, time, img)
        shutil.move(img, timepath)
    print("完成！")


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], 'o:i:', ["help"])
    for opt, arg in opts:
        if opt == '-i':
            in_path = arg
        elif opt == '-o':
            out_path = arg
        elif opt == '--help':
            print('-o 输出文件夹路径 -i 输入图片源文件夹路径')
            exit()
    if in_path != '' and out_path != '':
        main()
    else:
        print('缺少重要参数：\n -o 输出文件夹路径 -i 输入图片源文件夹路径')
