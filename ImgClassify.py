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

    if longitude == 0 or latitude == 0:
        return ''

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
    make = tags.get('Image Make', None)
    model = tags.get('Image Model', None)

    try:
        image_time = getExifTime(tags)
        if '' != image_time:
            time = image_time
        else:
            time = format_time(os.path.getmtime(filePath))
    except:
        time = format_time(os.path.getmtime(filePath))
        pass

    location = getLocation(GPSLatitude, GPSLongitude)

    if location == '':
        if (make is not None) and (model is not None):
            make.values = make.values.strip()
            model.values = model.values.strip()
            if make.values == '':
                return 'other', time
            if model.values == '':
                model.values = 'unknow'
            devName = make.values + "-" + model.values
            return devName, time
        else:
            return 'other', time
    else:
        return location, time


def getExifTime(tags):
    time = ''
    try:
        time = tags.get('Image DateTime').values.replace(':', '-')[:10]
    except:
        try:
            time = tags.get('EXIF DateTimeOriginal').values.replace(':', '-')[:10]
        except:
            try:
                time = tags.get('EXIF DateTimeDigitized').values.replace(':', '-')[:10]
            except:
                pass
            pass
        pass
    return time


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

    print("开始移动到 -->", in_path)
    for img, i in zip(fileList, range(len(fileList))):
        tag, time = getTimeAndDesc(img)
        if tag == '':
            tag = 'other'
        if time == '':
            time = "notime"
        if (img.endswith('mp4')):
            tag = '视频'
        if (img.endswith('zip')):
            tag = 'zip'
        tag = tag.strip()
        time = time.strip()
        timepath = out_path + '/' + tag + "/" + time
        mkdir(timepath)

        # 将这个文件移动到timedir
        try:
            shutil.move(img, timepath)
            print('[成功]', i + 1, "/", fileList.__len__(), tag, time, img)
        except:
            try:
                mkdir(out_path + '/重复文件/' + tag + "/" + time)
                shutil.move(img, out_path + '/重复文件/' + tag + "/" + time)
                print('[重复]', i + 1, "/", fileList.__len__(), tag, time, img)
            except:
                print('[错误]', i + 1, "/", fileList.__len__(), tag, time, img)
                pass
            pass
    print("完成！")


def mkdir(timepath):
    if not os.path.exists(timepath) or not os.path.isdir(timepath):
        # 新建文件夹
        os.makedirs(timepath, mode=0o777, exist_ok=True)


if __name__ == '__main__':
    in_path = out_path = ''
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
