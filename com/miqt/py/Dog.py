#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Dog:
    '类的帮助信息'  # 类文档字符串
    name = 0  # 类体

    def __init__(self, name):
        self.name = name

    def wang(self):
        print(self.name + "旺旺!")


xiaohuang = Dog("小黄")
xiaohuang.wang()


class HsqDog(Dog):
    def __init__(self, name):
        self.name = name

    def hehe(self):
        print(self.name + "!")


h = HsqDog("erha")
h.wang()
h.hehe()
