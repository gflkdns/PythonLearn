import pythoncom
import PyHook3
import threading
import time
from lol import mouse_move
import sys, getopt

# 每秒攻击次数
英雄攻速 = 1.5
# 每次攻击占用分为前摇/后摇，0-1
前摇比例 = 0.3
# 攻击后多移动一段时间
移动补偿 = 0

leftPass = False
# 是否只以英雄为目标 c
onlyLoL = True


def parseArg():
    print("使用说明：xxx.exe -g 英雄攻速 -q 前摇比例 -b 移动补偿")
    global 英雄攻速, 前摇比例, 移动补偿
    opts, args = getopt.getopt(sys.argv[1:], 'n:v:r:', [])
    for opt, arg in opts:
        if opt == '-g':
            英雄攻速 = arg
        elif opt == '-q':
            前摇比例 = arg
        elif opt == '-b':
            移动补偿 = arg

    print('英雄攻速：', 英雄攻速)
    print('攻击前摇：', 前摇比例)
    print('移动补偿：', 移动补偿)


def onMouseLeftDown(event):
    global leftPass
    leftPass = True
    return True


def onMouseLeftUp(event):
    global leftPass
    leftPass = False
    return True


def onKeyDown(event):
    if (event.Key == "Lshift"):
        global leftPass
        leftPass = True
    return True


def onKeyUp(event):
    if (event.Key == "Lshift"):
        global leftPass
        leftPass = False
    return True


def action():
    while True:
        global leftPass
        if leftPass:
            if onlyLoL:
                mouse_move.sendkey(0x2e, 1)
            qianyao = (1.0 / 英雄攻速) * (前摇比例)
            houyao = (1.0 / 英雄攻速) * (1 - 前摇比例) + 移动补偿
            message("开始平A【z】")
            mouse_move.sendkey(0x2c, 1)
            mouse_move.sendkey(0x2c, 0)
            message("等待前摇结束【{攻击前摇}】".format(攻击前摇=qianyao))
            time.sleep(qianyao)
            message("移动人物,取消后摇【X】")
            mouse_move.sendkey(0x2d, 1)
            mouse_move.sendkey(0x2d, 0)
            message("等待下一次攻击【{攻击间隔}】".format(攻击间隔=houyao))
            time.sleep(houyao)
            if onlyLoL:
                mouse_move.sendkey(0x2e, 0)
        else:
            time.sleep(0.05)


def keyLinster():
    # 创建一个“钩子”管理对象
    hm = PyHook3.HookManager()
    # 监听所有键盘事件
    hm.KeyDown = onKeyDown
    hm.KeyUp = onKeyUp
    # 设置键盘“钩子”q
    hm.HookKeyboard()
    # 监听所有鼠标事件
    hm.MouseLeftDown = onMouseLeftDown
    hm.MouseLeftUp = onMouseLeftUp
    # 设置鼠标“钩子”
    hm.HookMouse()
    # 进入循环，如不手动关闭，程序将一直处于监听状态
    pythoncom.PumpMessages()


def message(text):
    print(text)


def main():
    parseArg()
    threading.Thread(target=action).start()
    threading.Thread(target=keyLinster).start()


main()
