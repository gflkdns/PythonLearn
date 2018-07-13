
import os
import shutil
import datetime
import sys, getopt

'''
make.py -v [versionName] -n [releaseNote] -r [outPath] --d
'''
# 脚本配置
versions = 'v9.0.1'  # SDK版本 可使用命令 -v ... 设置
root = './luomi'  # 保存sdk相关文件的目录 可使用命令 -r ... 设置
releaseNote = '暂无版本说明'  # 可使用命令 -n ... 设置
onlydex = False  # 可使用命令 --onlydex ... 设置
salt = 0x2

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
    os.system(cmd)
    # cmd = "jar tvf {dexPath}".format(dexPath=dexPath)
    # os.system(cmd)


def makeAar():
    if os.path.exists(assetsPath):
        os.remove(assetsPath)
    intputfile = dexPath
    outputfile = assetsPath
    with open(intputfile, "rb") as input, open(outputfile, 'wb') as output:
        for i in input:
            for byte in i:
                output.write(bytes([byte ^ salt]))
    print('dex encode success!')
    cmd = 'gradlew luomilib:assembleRelease'
    os.system(cmd)
    if os.path.exists(aarPath):
        os.remove(aarPath)
    os.rename(releaseAarPath, aarPath)


def parseArg():
    global releaseNote, versions, root, dexPath, aarPath, logFilePath, onlydex
    opts, args = getopt.getopt(sys.argv[1:], 'n:v:r:', ["d"])
    for opt, arg in opts:
        if opt == '-n':
            releaseNote = arg
        elif opt == '-v':
            versions = arg
        elif opt == '-r':
            root = arg
        elif opt == '--d':
            onlydex = True
    dexPath = '{root}/luomi_{versions}.dex'.format(root=root, versions=versions)
    aarPath = '{root}/luomi_{versions}.aar'.format(root=root, versions=versions)
    logFilePath = '{root}/打包日志.txt'.format(root=root)


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
if __name__ == '__main__':
    parseArg()
    start_time = datetime.datetime.now()
    print('----------构建开始------------')
    init()
    print('----------build清除完成-------')
    makedex()
    print('----------dex打包完成---------')
    if not onlydex:
        makeAar()
    build_time = datetime.datetime.now() - start_time
    saveLog()

    print('----------构建结束,用时{time}------------'.format(time=build_time))
    print('----------save dir = {root}'.format(root=root))
