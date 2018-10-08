# !/usr/bin/python3
# coding: utf-8
import os
import re
import shutil
import datetime
import sys, getopt
from ftp import ftp_config
from ftp import ftp_client

'''
运行环境：
Python v3.6.4 并配置环境变量
import中对应的三方库
java 1.7+ 并配置环境变量
android studio 中的 gradlew工具，linux中使用gradlew.bat

使用方法：
打开cmd终端cd到项目目录，运行以下命令：

python make.py -v [版本名] -n [版本说明] -r [输出目录] --d  --ftp

-v [版本名]
-n [版本说明]
-r [输出目录]
--d 不需要传参，代表是否仅生成dex
--ftp 是否将生成的dex上传到指定ftp服务器
'''
# 脚本配置
versions = 'v9.0.1'  # SDK版本 可使用命令 -v ... 设置
root = './luomi'  # 保存sdk相关文件的目录 可使用命令 -r ... 设置
releaseNote = '暂无版本说明'  # 可使用命令 -n ... 设置
onlydex = False  # 可使用命令 --onlydex ... 设置
isUploadDexToFtp = False  # 可使用命令 --ftp ... 设置
salt = 0x2  # 加密盐

# 固定的文件路径
assetsPath = "./luomilib/src/main/assets/gg.png"  # assets下的dex文件名称
dexPath = '{root}/luomi_{versions}.dex'.format(root=root, versions=versions)
aarPath = '{root}/luomi_{versions}.aar'.format(root=root, versions=versions)
logFilePath = '{root}/打包日志.txt'.format(root=root)
clearPaths = [
    "./build",
    "./luomidex/build",
    "./luomilib/build",
]
jarPath = './luomidex/build/intermediates/bundles/release/classes.jar'
releaseAarPath = './luomilib/build/outputs/aar/luomilib-release.aar'

build_result = {}


def init():
    if not os.path.exists(root):
        os.makedirs(root)
    for i in clearPaths:
        if os.path.exists(i):
            shutil.rmtree(i)


def makedex():
    if os.path.exists(dexPath):
        os.remove(dexPath)
    cmd = 'gradlew luomidex:assembleRelease'
    os.system(cmd)
    cmd = "dx --dex --output={dexPath} {jarPath}".format(dexPath=dexPath, jarPath=jarPath)
    build_result['makedex'] = os.system(cmd)
    # cmd = "jar tvf {dexPath}".format(dexPath=dexPath)
    # os.system(cmd)


def makeAar():
    if os.path.exists(assetsPath):
        os.remove(assetsPath)
    intputfile = dexPath
    outputfile = assetsPath
    img = [137, 80, 78, 71, 13, 10, 26, 10, 0, 0, 0, 13, 73, 72, 68, 82
        , 0, 0, 0, 16, 0, 0, 0, 16, 8, 6, 0, 0, 0, 31, 243, 255
        , 97, 0, 0, 1, 228, 73, 68, 65, 84, 56, 79, 165, 147, 63, 136, 19
        , 81, 16, 198, 191, 121, 75, 32, 198, 35, 71, 64, 16, 66, 84, 12, 106
        , 178, 251, 30, 90, 164, 149, 67, 80, 16, 17, 11, 155, 179, 240, 206, 195
        , 230, 44, 181, 20, 65, 212, 230, 14, 59, 237, 212, 66, 241, 244, 132, 139
        , 197, 21, 118, 254, 1, 139, 107, 3, 130, 243, 54, 201, 17, 35, 88, 4
        , 180, 9, 66, 84, 150, 176, 59, 178, 97, 3, 113, 145, 211, 211, 215, 60
        , 134, 239, 205, 143, 111, 230, 205, 16, 82, 199, 24, 179, 7, 192, 57, 0
        , 187, 69, 228, 32, 128, 93, 68, 244, 3, 192, 75, 17, 89, 179, 214, 126
        , 154, 76, 161, 113, 160, 181, 158, 34, 162, 39, 0, 190, 13, 135, 195, 235
        , 237, 118, 251, 227, 88, 171, 213, 106, 153, 32, 8, 142, 0, 184, 2, 96
        , 167, 136, 204, 91, 107, 7, 177, 62, 2, 20, 139, 197, 92, 161, 80, 120
        , 33, 34, 75, 190, 239, 191, 73, 187, 154, 140, 181, 214, 11, 0, 46, 247
        , 251, 253, 163, 189, 94, 239, 251, 8, 160, 181, 126, 16, 69, 81, 189, 217
        , 108, 190, 222, 42, 121, 172, 121, 158, 55, 71, 68, 51, 214, 218, 69, 242
        , 60, 239, 128, 82, 234, 38, 51, 207, 253, 77, 242, 68, 201, 171, 34, 114
        , 131, 180, 214, 203, 97, 24, 62, 106, 181, 90, 155, 219, 1, 84, 171, 213
        , 67, 142, 227, 92, 36, 99, 204, 26, 51, 199, 93, 135, 49, 230, 109, 124
        , 51, 243, 177, 223, 193, 210, 186, 49, 166, 30, 3, 214, 153, 249, 236, 63
        , 2, 214, 99, 64, 157, 153, 103, 183, 99, 127, 162, 15, 207, 255, 31, 160
        , 181, 190, 45, 34, 43, 190, 239, 219, 63, 185, 40, 151, 203, 211, 221, 110
        , 247, 107, 242, 245, 30, 128, 5, 114, 93, 119, 159, 82, 106, 201, 90, 123
        , 62, 233, 195, 188, 136, 204, 16, 209, 234, 96, 48, 120, 151, 205, 102, 29
        , 199, 113, 14, 3, 88, 36, 162, 87, 204, 252, 48, 1, 60, 3, 112, 117
        , 52, 72, 198, 152, 123, 81, 20, 109, 248, 190, 255, 52, 142, 75, 165, 210
        , 142, 124, 62, 127, 134, 136, 78, 3, 152, 22, 145, 77, 165, 212, 125, 102
        , 254, 16, 235, 158, 231, 29, 39, 162, 89, 107, 237, 165, 201, 81, 222, 0
        , 112, 215, 90, 251, 120, 171, 82, 92, 215, 61, 161, 148, 186, 22, 4, 193
        , 169, 78, 167, 19, 164, 151, 105, 5, 192, 32, 12, 195, 59, 185, 92, 238
        , 125, 163, 209, 24, 142, 97, 149, 74, 101, 127, 38, 147, 185, 5, 96, 74
        , 68, 46, 252, 178, 76, 169, 101, 217, 27, 219, 3, 112, 50, 121, 252, 57
        , 41, 225, 139, 136, 212, 211, 235, 252, 19, 212, 108, 216, 29, 124, 249, 35
        , 153, 0, 0, 0, 0, 73, 69, 78, 68, 174, 66, 96, 130]
    with open(intputfile, "rb") as input, open(outputfile, 'wb') as output:
        for i in img:
            output.write(bytes([i]))
        for i in input:
            for byte in i:
                output.write(bytes([byte ^ salt]))
    print('dex encode success!')
    cmd = 'gradlew luomilib:assembleRelease'
    build_result['makeaar'] = os.system(cmd)
    if os.path.exists(aarPath):
        os.remove(aarPath)
    os.rename(releaseAarPath, aarPath)


def parseArg():
    global releaseNote, versions, root, dexPath, aarPath, logFilePath, onlydex, isUploadDexToFtp
    opts, args = getopt.getopt(sys.argv[1:], 'n:v:r:', ["d", "ftp"])
    for opt, arg in opts:
        if opt == '-n':
            releaseNote = arg
        elif opt == '-v':
            versions = arg
        elif opt == '-r':
            root = arg
        elif opt == '--d':
            onlydex = True
        elif opt == '--ftp':
            isUploadDexToFtp = True
    dexPath = '{root}/luomi_{versions}.dex'.format(root=root, versions=versions)
    aarPath = '{root}/luomi_{versions}.aar'.format(root=root, versions=versions)
    logFilePath = '{root}/打包日志.txt'.format(root=root)
    build_result['opts'] = opts
    build_result['args'] = args
    build_result['releaseNote'] = releaseNote


def saveLog():
    with open(logFilePath, "a+", encoding='utf-8') as f:
        f.seek(0)
        f.write("-----------------------------\n")
        f.write("打包时间： {v}  \n".format(v=datetime.datetime.now()))
        f.write("版本： {v}  \n".format(v=versions))
        f.write("打包用时： {v}  \n".format(v=build_time))
        f.write("dex路径： {v}  \n".format(v=dexPath))
        if not onlydex:
            f.write("aar路径： {v}  \n".format(v=aarPath))
        f.write("版本说明： {v}  \n".format(v=releaseNote))
        f.write("打包结果:{v}  \n".format(v=build_result))


def replaceFile(filepath, pattern, repl):
    with open(filepath, 'r+', encoding='utf-8') as f:
        str = f.read()
        if str.find('//target') != -1:
            result, number = re.subn(pattern, repl, str)
        print(result)
        print(number)
        f.seek(0)
        f.truncate(len(str))
        f.write(result)
    build_result['replaceFile'] = 'success'


def uploadDex():
    result = ftp_client.getConnect(
        host=ftp_config.host,
        port=ftp_config.port,
        username=ftp_config.username,
        password=ftp_config.password
    )

    if result[0] != 1:
        print(result[1])
        print("connection error")
    else:
        print("connection success")
        ftp = result[2]
        result = ftp_client.uploadFile(
            ftp=ftp,
            remoteRelDir=ftp_config.homeDir,
            localAbsPath=dexPath
        )
        ftp.quit()
        print("全部成功" if result[0] == 1 else "部分失败")
        print(result[1])
    build_result['uploadDex'] = result

def git_tag():
    print('-----创建Git Tag-----')
    cmd = 'git tag -a {v} -m {m}'.format(v=versions, m=releaseNote)
    os.system(cmd)
    if isUploadDexToFtp:
        # 如果上传dex到ftp，那么也上传这个标签到远程仓库比较好
        print('-----验证仓库权限-----')
        cmd = 'git push origin {v}'.format(v=versions)
        os.system(cmd)


if __name__ == '__main__':
    parseArg()
    start_time = datetime.datetime.now()
    print('----------构建开始------------')
    replaceFile('./luomidex/src/main/java/com/hz/yl/DexCfg.java', r'"dex_.*"',
                '"dex_{versions}"'.format(versions=versions))
    replaceFile('./luomilib/src/main/java/com/hz/yl/LibCfg.java', r'"lib_.*"',
                '"lib_{versions}"'.format(versions=versions))
    init()
    print('----------build清除完成-------')
    makedex()
    if isUploadDexToFtp:
        uploadDex()
    print('----------dex打包完成---------')
    if not onlydex:
        makeAar()
    build_time = datetime.datetime.now() - start_time
    saveLog()
    git_tag()

    print('----------构建结束,用时{time}------------'.format(time=build_time))
    print('----------save dir = {root}'.format(root=root))
    print(build_result)
