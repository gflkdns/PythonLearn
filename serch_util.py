# -*- coding: utf-8 -*-

import pyperclip
import pythoncom
import PyHook3
import threading
import sys
import webbrowser

cur_event = None
last_event = None


def onMouseEvent(event):
    # 返回 True 以便将事件传给其它处理程序
    # 注意，这儿如果返回 False ，则鼠标事件将被全部拦截
    # 也就是说你的鼠标看起来会僵在那儿，似乎失去响应了
    return True


def onKeyboardEvent(event):
    # 同鼠标事件监听函数的返回值
    global cur_event
    cur_event = event
    return True


def loopKeyboardEvent():
    global cur_event
    global last_event
    while True:
        if cur_event != last_event:
            if last_event == 'Rcontrol' and cur_event == 'C':
                value = pyperclip.paste()
                print('捕获到粘贴板：', value)
                url = input_url.replace('参数', value)
                print('开始打开链接：', url)
                webbrowser.open(url=url, new=0, autoraise=True)
            last_event = cur_event


def loopMouseEvent():
    global cur_event
    global last_event
    while True:
        if cur_event != last_event:
            print(cur_event)
            last_event = cur_event


input_url = ""


def main():
    print('.....使用帮助.........')
    print('打开本软件后，本软件会监听你的粘贴板\n当你按下键盘右边的的ctrl按键，则会打开预设的网址')
    print('百度为例，输入“https://www.baidu.com/s?wd=参数”，则当你按下ctrl的时候，\n本软件会自动把你的粘贴板中的内容复制到参数（参数是固定的）的位置，然后打开这个链接')
    print('比如你输入了“山东”，则打开的链接为https://www.baidu.com/s?wd=山东,依次类推')
    print('.....................')
    global input_url
    print('输入一个链接：格式按照 https://www.baidu.com/s?wd=参数')
    input_url = input()
    if not input_url.startswith('http'):
        print('输入的链接不对')
        return
    print('已经开始运行了')
    t1 = threading.Thread(target=loopKeyboardEvent, name="loopKeyboardEvent")
    t2 = threading.Thread(target=loopMouseEvent, name="loopMouseEvent")
    t1.start()
    # t2.start()
    # t1.join()
    # t2.join()
    # 创建一个“钩子”管理对象
    hm = PyHook3.HookManager()

    # 监听所有键盘事件
    hm.KeyDown = onKeyboardEvent
    # 设置键盘“钩子”
    hm.HookKeyboard()

    # # 监听所有鼠标事件
    # hm.MouseAll = onMouseEvent
    # # 设置鼠标“钩子”
    # hm.HookMouse()

    # 进入循环，如不手动关闭，程序将一直处于监听状态
    pythoncom.PumpMessages()


if __name__ == "__main__":
    main()
