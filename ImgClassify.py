# !/usr/bin/python
# -*- coding:utf8 -*-
import getopt
import time

import shutil, os

import sys

allFileNum = 0


def printPath(level, path):
    global allFileNum
    ''''' 
    打印一个目录下的所有文件夹和文件 
    '''
    # 所有文件夹，第一个字段是次目录的级别
    dirList = []
    # 所有文件
    fileList = []
    # 返回一个列表，其中包含在目录条目的名称(google翻译)
    files = os.listdir(path)
    # 先添加目录级别
    dirList.append(str(level))
    for f in files:
        if (os.path.isdir(path + '/' + f)):
            # 排除隐藏文件夹。因为隐藏文件夹过多
            if (f[0] == '.'):
                pass
            else:
                # 添加非隐藏文件夹
                dirList.append(f)
        if (os.path.isfile(path + '/' + f)):
            # 添加文件
            fileList.append(f)
            # 当一个标志使用，文件夹列表第一个级别不打印
    i_dl = 0
    for dl in dirList:
        if (i_dl == 0):
            i_dl = i_dl + 1
        else:
            # 打印至控制台，不是第一个的目录
            print('-' * (int(dirList[0])), dl)
            # 打印目录下的所有文件夹和文件，目录级别+1
            printPath((int(dirList[0]) + 1), path + '/' + dl)
    for fl in fileList:
        # 打印文件
        print('-' * (int(dirList[0])), fl)
        # 随便计算一下有多少个文件
        allFileNum = allFileNum + 1


def get_FileCreateTime(filePath):
    t = os.path.getmtime(filePath)
    return TimeStampToTime(t)


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    # return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)
    return time.strftime('%Y-%m-%d', timeStruct)


def findFile(fileList, path):
    files = os.listdir(path)
    for f in files:
        if (os.path.isdir(path + '/' + f)):
            # 排除隐藏文件夹。因为隐藏文件夹过多
            if (f[0] == '.'):
                pass
            else:
                # 添加非隐藏文件夹
                findFile(fileList, path + '/' + f)
        if (os.path.isfile(path + '/' + f)):
            # 添加文件
            fileList.append(path + '/' + f)


in_path = ''
out_path = ''


def main():
    fileList = []

    findFile(fileList, in_path)
    print(fileList)

    timedir = []
    print("开始移动" + in_path)
    for img, i in zip(fileList, range(len(fileList))):
        time = get_FileCreateTime(img)
        timepath = out_path +'/'+ time
        if time not in timedir:
            # 新建这个日期的文件夹
            os.makedirs(timepath, mode=0o777, exist_ok=True)
            timedir.append(time)

        # 将这个文件移动到timedir
        print(i, "/", fileList.__len__())
        shutil.move(img, timepath)
    print("完成！")


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], 'o:i:', [ "help"])
    for opt, arg in opts:
        if opt == '-i':
            in_path = arg
        elif opt == '-o':
            out_path = arg
        elif opt == '--help':
            print('-o 输出文件夹路径 -i 输入图片源文件夹路径')
            exit()
    if in_path != '' and out_path!='':
        main()
    else:
        print('缺少重要参数：\n -o 输出文件夹路径 -i 输入图片源文件夹路径')
