#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : $lose.py
# @Author: Hu
# @Date  : 2018.10
# @Contact：pinckhu@sina.com
from PyQt5.QtCore import pyqtSignal,QThread
from time import sleep

'''
多线程收发消息
'''
# 创建一个多线程收发消息
class MyThread(QThread):
    # 定义信号,定义参数为str类型
    messageSignal = pyqtSignal(str)

    def __init__(self,connfd,mess):
        self.connfd = connfd
        self.message = mess
        super(MyThread, self).__init__()

    def run(self):
        # 启动多线程
        try:
            res = self.connfd.mess(self.message)
        except AttributeError:
            pass
        try:
            self.messageSignal.emit(res)
        except UnboundLocalError:
            pass

# 创建一个多线程信号
class Mytthread(QThread):
    # 定义信号,定义参数为int类型
    breakSignal = pyqtSignal(int)

    def __init__(self):
        super(Mytthread, self).__init__()

    def run(self):
        for i in range(60, -1, -1):
            # 发出信号
            self.breakSignal.emit(i)
            # 暂停一秒
            sleep(1)
        sleep(2)
        self.deleteLater()