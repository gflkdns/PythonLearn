import re
# 找到所有的app名称
def findApps(list, data):
    # 将NOR关键字分行处理，便于后续操作
    data = data.replace('[NOR]', '\n[NOR]')
    rcode = r'\b' + startcfg + r'.*?' + endcfg + r'\b'
    a = re.findall(rcode, data, flags=0)
    for i in a:
        # 裁剪字符串
        s=i.find(']')+1
        e=i.find('[')
        appname = i[s:e]
        if (len(appname) != 0):
            list.append(appname)


def getFileContext(path):
    f = open(path, "r", encoding='utf-8')
    data = f.read()
    return data


def main():
    # 读取文件
    data = getFileContext(path)
    # 正则表达式匹配
    apps = []
    findApps(apps, data)
    # 去除重复并且判断出现了多少次
    res = []
    for i in apps:
        if not res.__contains__(i):
            res.append(i)
    # 输出结果
    print("整个文档共包含", res.__len__(), "个",[startcfg],[endcfg])
    for i in res:
        print(i, '共出现', apps.count(i), '次')


# 配置參數——START
path = "F:\PythonPoj\PythonLearn\正则靶标.txt"      #文件路径
startcfg = 'NOR'                                        #头关键字
endcfg = 'ENT.TV'                                       #尾关键字
# 配置蠶食——END
main()
