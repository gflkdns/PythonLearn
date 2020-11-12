import pythoncom
import PyHook3
import threading
import time
import wx
import getopt
import sys
from ctypes import POINTER, c_ulong, Structure, c_ushort, c_short, c_long, byref, windll, pointer, sizeof, Union

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


# -------------------点击工具类-----------------------


# -------------------UI-----------------------------
class MainWindow(wx.Frame):
    # 点击间隔
    minTime = 0.1
    leftPass = False
    # 是否只以英雄为目标 c
    onlyLoL = True

    def onKeyDown(self, event):
        if (event.Key == "Lshift"):
            self.leftPass = True
        return True

    def onKeyUp(self, event):
        if (event.Key == "Lshift"):
            self.leftPass = False
        return True

    def action(self):
        while True:
            if self.leftPass and not self.isPause:
                # 每秒攻击次数
                英雄攻速 = float(self.text_num1.Label)
                # 每次攻击占用分为前摇/后摇，0-1
                前摇比例 = float(self.text_num2.Label)
                # 攻击后多移动一段时间
                移动补偿 = float(self.text_num3.Label)

                if self.onlyLoL:
                    sendkey(0x2e, 1)
                qianyao = (1.0 / 英雄攻速) * (前摇比例)
                houyao = (1.0 / 英雄攻速) * (1 - 前摇比例) + 移动补偿
                # 开始攻击，并等待前摇结束
                print("开始攻击，并等待前摇结束[{攻击前摇}]".format(攻击前摇=qianyao))
                self.click(0x2c, qianyao)
                # 移动人物,取消后摇，并走动攻击间隔的时间
                print("等待下一次攻击[{攻击间隔}]\n".format(攻击间隔=houyao))
                self.click(0x2d, houyao)
                if self.onlyLoL:
                    sendkey(0x2e, 0)
            else:
                time.sleep(0.05)

    # 把时间切分开，快速点击
    def click(self, key, clicktime):
        freeTime = clicktime
        # 0.25 - 0.1 - 0.1 - 0.05
        # 松开走A按键立即停止点击
        while freeTime > self.minTime and self.leftPass:
            sendkey(key, 1)
            sendkey(key, 0)
            time.sleep(self.minTime)
            freeTime = freeTime - self.minTime
        sendkey(key, 1)
        sendkey(key, 0)
        time.sleep(self.minTime)

    def keyLinster(self, ):
        # 创建一个“钩子”管理对象
        hm = PyHook3.HookManager()
        # 监听所有键盘事件
        hm.KeyDown = self.onKeyDown
        hm.KeyUp = self.onKeyUp
        # 设置键盘“钩子”q
        hm.HookKeyboard()
        # 进入循环，如不手动关闭，程序将一直处于监听状态
        pythoncom.PumpMessages()

    def message(self, text):
        self.message_text.Label = self.message_text.Label[0:10]
        self.message_text.Label = text + self.message_text.Label

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, style=wx.DEFAULT_FRAME_STYLE ^ (
                wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU) | wx.STAY_ON_TOP,
                          size=(170, 180))
        self.SetTransparent(180)  # 设置透明

        self.isPause = True

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer5 = wx.BoxSizer(wx.HORIZONTAL)

        self.text1 = wx.StaticText(self, name="aa", label="英雄攻速", size=(60, -1), style=wx.ALIGN_CENTER)
        self.text_num1 = wx.StaticText(self, name="aa", label="0.7", size=(30, -1), style=wx.ALIGN_CENTER)
        self.text1.SetForegroundColour('blue')
        self.text_num1.SetForegroundColour('red')
        self.button_up1 = wx.Button(self, name="up1", label="+", size=(30, 30))
        self.button_down1 = wx.Button(self, name="down1", label="-", size=(30, 30))
        self.Bind(wx.EVT_BUTTON, self.onClick, self.button_up1)
        self.Bind(wx.EVT_BUTTON, self.onClick, self.button_down1)
        self.sizer1.Add(self.text1, flag=wx.ALIGN_CENTER)
        self.sizer1.Add(self.text_num1, flag=wx.ALIGN_CENTER)
        self.sizer1.Add(self.button_up1, flag=wx.ALIGN_CENTER)
        self.sizer1.Add(self.button_down1, flag=wx.ALIGN_CENTER)

        self.text2 = wx.StaticText(self, name="aa", label="前摇间隔", size=(60, -1), style=wx.ALIGN_CENTER)
        self.text_num2 = wx.StaticText(self, name="aa", label="0.3", size=(30, -1), style=wx.ALIGN_CENTER)
        self.text2.SetForegroundColour('blue')
        self.text_num2.SetForegroundColour('red')
        self.button_up2 = wx.Button(self, name="up2", label="+", size=(30, 30))
        self.button_down2 = wx.Button(self, name="down2", label="-", size=(30, 30))
        self.Bind(wx.EVT_BUTTON, self.onClick, self.button_up2)
        self.Bind(wx.EVT_BUTTON, self.onClick, self.button_down2)
        self.sizer2.Add(self.text2, flag=wx.ALIGN_CENTER)
        self.sizer2.Add(self.text_num2, flag=wx.ALIGN_CENTER)
        self.sizer2.Add(self.button_up2, flag=wx.ALIGN_CENTER)
        self.sizer2.Add(self.button_down2, flag=wx.ALIGN_CENTER)

        self.text3 = wx.StaticText(self, name="aa", label="移动补偿", size=(60, -1), style=wx.ALIGN_CENTER)
        self.text_num3 = wx.StaticText(self, name="aa", label="0.0", size=(30, -1), style=wx.ALIGN_CENTER)
        self.text3.SetForegroundColour('blue')
        self.text_num3.SetForegroundColour('red')
        self.button_up3 = wx.Button(self, name="up3", label="+", size=(30, 30))
        self.button_down3 = wx.Button(self, name="down3", label="-", size=(30, 30))
        self.Bind(wx.EVT_BUTTON, self.onClick, self.button_up3)
        self.Bind(wx.EVT_BUTTON, self.onClick, self.button_down3)
        self.sizer3.Add(self.text3, flag=wx.ALIGN_CENTER)
        self.sizer3.Add(self.text_num3, flag=wx.ALIGN_CENTER)
        self.sizer3.Add(self.button_up3, flag=wx.ALIGN_CENTER)
        self.sizer3.Add(self.button_down3, flag=wx.ALIGN_CENTER)

        self.button_start = wx.Button(self, name="start", label="启动", size=(150 / 2, 30))
        self.button_stop = wx.Button(self, name="stop", label="关闭", size=(150 / 2, 30))
        self.Bind(wx.EVT_BUTTON, self.onClick, self.button_start)
        self.Bind(wx.EVT_BUTTON, self.onClick, self.button_stop)
        self.sizer4.Add(self.button_start, flag=wx.ALIGN_CENTER)
        self.sizer4.Add(self.button_stop, flag=wx.ALIGN_CENTER)

        self.message_text = wx.StaticText(self, name="aa", label="作者:github.com/miqt")
        self.message_text.SetForegroundColour('red')
        self.sizer5.Add(self.message_text)

        self.sizer.Add(self.sizer1)
        self.sizer.Add(self.sizer2)
        self.sizer.Add(self.sizer3)
        self.sizer.Add(self.sizer4)
        self.sizer.Add(self.sizer5)

        self.SetSizer(self.sizer)
        self.Show(True)

        self.thread_key = threading.Thread(target=self.action)
        self.thread_action = threading.Thread(target=self.keyLinster)
        self.thread_key.daemon = True
        self.thread_action.daemon = True
        self.thread_key.start()
        self.thread_action.start()

    def onClick(self, event):
        name = event.GetEventObject().GetName()
        if name == "up1":
            self.updateNum(self.text_num1, True, 0.1, 3.0, 0.1)
        elif name == "down1":
            self.updateNum(self.text_num1, False, 0.1, 3.0, 0.1)
        elif name == "up2":
            self.updateNum(self.text_num2, True, 0.1, 0.9, 0.05)
        elif name == "down2":
            self.updateNum(self.text_num2, False, 0.1, 0.9, 0.05)
        elif name == "up3":
            self.updateNum(self.text_num3, True, 0.0, 3.0, 0.1)
        elif name == "down3":
            self.updateNum(self.text_num3, False, 0.0, 3.0, 0.1)
        elif name == "start":
            self.message_text.Label = "已启动,按住Shift或T走A"
            self.isPause = False
            pass
        elif name == "stop":
            self.isPause = True
            pass

    def updateNum(self, who, isUp, min, max, min_diff):
        if isUp:
            num = float(who.Label) + min_diff
        else:
            num = float(who.Label) - min_diff
        num = round(num, 2)
        if num < min:
            num = min
        if num > max:
            num = max
        num = str(num)
        if len(num) > 3:
            num = num[0:4]
        who.SetLabel(num)


app = wx.App(False)  # 创建1个APP，禁用stdout/stderr重定向
ui = MainWindow(None, "摇头怪!")  # 这是一个顶层的window
app.MainLoop()
