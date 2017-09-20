import re

# 找到所有的app名称
from collections import Counter


def findApps(list, data):
    # 将NOR关键字分行处理，便于后续操作
    data = data.replace('[NOR]', '\n[NOR]')
    rcode = r'\b' + start + r'.*?' + end + r'\b'
    a = re.findall(rcode, data, flags=0)
    for i in a:
        # 裁剪字符串
        s = i.find(']') + 1
        e = i.find('[')
        app_name = i[s:e]
        if len(app_name) != 0:
            list.append(app_name)

def openFile(path):
    f = open(path, "r", encoding='utf-8')
    data = f.read()
    return data


def main():
    # 读取文件
    data = openFile(path)
    # 正则表达式匹配
    apps = []
    findApps(apps, data)
    # 计数
    a = Counter(apps)
    a = a.most_common()
    # 输出结果
    for i in a:
        print(i)


# 配置參數——START
path = "F:\PythonPoj\PythonLearn\正则靶标.txt"  # 文件路径
start = 'NOR'  # 头关键字
end = 'LOC.CATER'  # 尾关键字
# 配置蠶食——END
main()
