import pythoncom
import PyHook3
import threading
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import time
import wx
import os

# 每秒攻击次数
英雄攻速 = 1.5
# 每次攻击占用分为前摇/后摇，0-1
前摇比例 = 0.3
# 攻击后多移动一段时间
移动补偿 = 0

print('攻速：', 英雄攻速)
print('攻击前摇：', 前摇比例)

leftPass = False
# 是否只以英雄为目标 c
onlyLoL = True


# --------------------------------------------------
class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(250, 550))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.textInput1 = wx.TextCtrl(self, name="英雄攻速", value=str(英雄攻速), size=(125, 25))
        self.textInput2 = wx.TextCtrl(self, name="前摇比例", value=str(前摇比例), size=(125, 25))
        self.textInput3 = wx.TextCtrl(self, name="移动补偿", value=str(移动补偿), size=(125, 25))

        self.text1 = wx.StaticText(self, -1, "英雄攻速", size=(125, 25), style=wx.ALIGN_CENTER)
        self.text2 = wx.StaticText(self, -1, "前摇比例", size=(125, 25), style=wx.ALIGN_CENTER)
        self.text3 = wx.StaticText(self, -1, "移动补偿", size=(125, 25), style=wx.ALIGN_CENTER)
        self.text4 = wx.StaticText(self, -1, "", size=(250, 400))
        self.text4.SetForegroundColour("White")
        self.text4.SetBackgroundColour("Black")
        self.text4.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL))

        self.sizer1.Add(self.textInput1)
        self.sizer2.Add(self.textInput2)
        self.sizer3.Add(self.textInput3)

        self.sizer1.Add(self.text1)
        self.sizer2.Add(self.text2)
        self.sizer3.Add(self.text3)

        self.sizer.Add(self.sizer1)
        self.sizer.Add(self.sizer2)
        self.sizer.Add(self.sizer3)

        self.button_enter = wx.Button(self, name="确定", label='修改参数', size=(250, 25))
        self.button_start = wx.Button(self, name="确定", label='修改参数', size=(250, 25))
        self.Bind(wx.EVT_BUTTON, self.onSetTime, self.button_enter)
        self.sizer.Add(self.button_enter)

        self.sizer.Add(self.text4)

        self.SetSizer(self.sizer)
        self.Show(True)

    def OnClose(self, event):
        print("exit")
        exit(0)

    def onSetTime(self, event):
        try:
            global 英雄攻速, 前摇比例, 移动补偿
            英雄攻速 = float(self.textInput1.Value)
            前摇比例 = float(self.textInput2.Value)
            移动补偿 = float(self.textInput3.Value)
        except:
            pass
        self.setMessage(
            '英雄攻速:' + str(英雄攻速) +
            '前摇比例:' + str(前摇比例) +
            '移动补偿:' + str(移动补偿)
        )
        pass

    def setMessage(self, text):
        self.text4.SetLabel(text + "\n" + self.text4.Label)


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


k = PyKeyboard()


def action():
    while True:
        global leftPass
        if leftPass:
            if onlyLoL:
                k.press_key('c')
            qianyao = (1.0 / 英雄攻速) * (前摇比例)
            houyao = (1.0 / 英雄攻速) * (1 - 前摇比例) + 移动补偿
            message("开始平A【z】")
            k.press_key('z')
            k.release_key('z')
            message("等待前摇结束【{攻击前摇}】".format(攻击前摇=qianyao))
            time.sleep(qianyao)
            message("移动人物,取消后摇【X】")
            k.press_key('x')
            k.release_key('x')
            message("等待下一次攻击【{攻击间隔}】".format(攻击间隔=houyao))
            time.sleep(houyao)
            if onlyLoL:
                k.release_key('c')
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


ui: MainWindow = None


def ui():
    global ui
    app = wx.App(False)  # 创建1个APP，禁用stdout/stderr重定向
    ui = MainWindow(None, "化身摇头怪!")  # 这是一个顶层的window
    app.MainLoop()


def message(text):
    print(text)
    if ui is not None:
        ui.setMessage(text)


def main():
    threading.Thread(target=ui).start()
    threading.Thread(target=action).start()
    threading.Thread(target=keyLinster).start()


main()
