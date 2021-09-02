import os
import re


def run_silently(cmd: str) -> str:
    """返回系统命令的执行结果"""
    with os.popen(cmd) as fp:
        bf = fp._stream.buffer.read()
    try:
        return bf.decode().strip()
    except UnicodeDecodeError:
        return bf.decode('gbk').strip()


print('APK DUMP TOOL START!')
print('https://github.com/miqt')

res = run_silently("adb shell dumpsys activity top")
# (ACTIVITY\s)(.*?)(/)(.*?)(\s.*?pid=)([0-9]+)
activitys = re.findall(r'(ACTIVITY\s)(.*?)(/)(.*?)(\s.*?pid=)([0-9]+)', res, 0)
print('---------------------CURRENT_TASK--------------------------')
for item in activitys:
    package = item[1]
    activity = item[3]
    pid = item[5]
    print(package, activity, pid)
print('-----------------------------------------------------------')
toppackage = activitys[activitys.count(activitys) - 1][1]
print('TOP TASK -->', toppackage)
res = run_silently("adb shell pm path " + toppackage)[8:]
print("PATH =", res)
print('-----------------------------------------------------------')
res = run_silently("adb pull " + res + " ./" + toppackage + ".apk")
print(res)
print('-----------------------------------------------------------')
print("DUMP SUCCESS")
os.system('pause')
