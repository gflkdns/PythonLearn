import getopt
import sys
import threading
import time
from ctypes import POINTER, c_ulong, Structure, c_ushort, c_short, c_long, byref, windll, pointer, sizeof, Union

import PyHook3
import pythoncom

# ---------------------------------------------

PUL = POINTER(c_ulong)


class KeyBdInput(Structure):
    _fields_ = [("wVk", c_ushort),
                ("wScan", c_ushort),
                ("dwFlags", c_ulong),
                ("time", c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(Structure):
    _fields_ = [("uMsg", c_ulong),
                ("wParamL", c_short),
                ("wParamH", c_ushort)]


class MouseInput(Structure):
    _fields_ = [("dx", c_long),
                ("dy", c_long),
                ("mouseData", c_ulong),
                ("dwFlags", c_ulong),
                ("time", c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(Structure):
    _fields_ = [("type", c_ulong),
                ("ii", Input_I)]


class POINT(Structure):
    _fields_ = [("x", c_ulong),
                ("y", c_ulong)]


# <Get Pos>
def get_mpos():
    orig = POINT()
    windll.user32.GetCursorPos(byref(orig))
    return int(orig.x), int(orig.y)


# </Get Pos>

# <Set Pos>
def set_mpos(pos):
    x, y = pos
    windll.user32.SetCursorPos(x, y)


# </Set Pos>

# <move and click>
def move_click(pos, move_back=False):
    origx, origy = get_mpos()
    set_mpos(pos)
    FInputs = Input * 2
    extra = c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, 2, 0, pointer(extra))
    ii2_ = Input_I()
    ii2_.mi = MouseInput(0, 0, 0, 4, 0, pointer(extra))
    x = FInputs((0, ii_), (0, ii2_))
    windll.user32.SendInput(2, pointer(x), sizeof(x[0]))
    if move_back:
        set_mpos((origx, origy))
        return origx, origy
    # </move and click>


def sendkey(scancode, pressed):
    FInputs = Input * 1
    extra = c_ulong(0)
    ii_ = Input_I()
    flag = 0x8  # KEY_SCANCODE
    ii_.ki = KeyBdInput(0, 0, flag, 0, pointer(extra))
    InputBox = FInputs((1, ii_))
    if scancode is None:
        return
    InputBox[0].ii.ki.wScan = scancode
    InputBox[0].ii.ki.dwFlags = 0x8
    # KEY_SCANCODE
    if not (pressed):
        InputBox[0].ii.ki.dwFlags |= 0x2
        # released
    windll.user32.SendInput(1, pointer(InputBox), sizeof(InputBox[0]))


# ---------------------------------------------

# 每秒攻击次数
英雄攻速 = 1.5
# 每次攻击占用分为前摇/后摇，0-1
前摇比例 = 0.3
# 攻击后多移动一段时间
移动补偿 = 0
# 点击间隔
minTime = 0.1

leftPass = False
# 是否只以英雄为目标 c
onlyLoL = True


def parseArg():
    print("使用说明：xxx.exe -g 英雄攻速 -q 前摇比例 -b 移动补偿 -d 点击间隔")
    global 英雄攻速, 前摇比例, 移动补偿, minTime
    opts, args = getopt.getopt(sys.argv[1:], 'g:q:b:d:', [])
    for opt, arg in opts:
        if opt == '-g':
            英雄攻速 = float(arg)
        elif opt == '-q':
            前摇比例 = float(arg)
        elif opt == '-b':
            移动补偿 = float(arg)
        elif opt == '-d':
            minTime = float(arg)

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
    if (event.Key == "T"):
        global leftPass
        leftPass = True
    return True


def onKeyUp(event):
    if (event.Key == "T"):
        global leftPass
        leftPass = False
    return True


def action():
    while True:
        global leftPass
        if leftPass:
            if onlyLoL:
                sendkey(0x2e, 1)
            qianyao = (1.0 / 英雄攻速) * (前摇比例)
            houyao = (1.0 / 英雄攻速) * (1 - 前摇比例) + 移动补偿
            message("开始平A[z]")
            message("等待前摇结束[{攻击前摇}]".format(攻击前摇=qianyao))
            click(0x2c, qianyao)
            message("移动人物,取消后摇[X]")
            message("等待下一次攻击[{攻击间隔}]\n".format(攻击间隔=houyao))
            click(0x2d, houyao)
            if onlyLoL:
                sendkey(0x2e, 0)
        else:
            time.sleep(0.05)


# 把时间切分开，快速点击
def click(key, clicktime):
    freeTime = clicktime
    # 0.25 - 0.1 - 0.1 - 0.05
    while freeTime > minTime:
        sendkey(key, 1)
        sendkey(key, 0)
        time.sleep(minTime)
        freeTime = freeTime - minTime
    sendkey(key, 1)
    sendkey(key, 0)
    time.sleep(minTime)


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
