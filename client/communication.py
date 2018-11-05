#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : $communication.py
# @Author: Hu
# @Date  : 2018.10

'''
客户端的消息收发
name:xxx
'''

from socket import *


# 创建一个客户端套接字
class MySocket(object):
    def __init__(self):
        self.addr = ('176.209.106.16',1080)
        self.sockfd = socket()
        self.sockfd.connect(self.addr)
    
    def mess(self,data):
        res = ''
        try:
            self.sockfd.send(data.encode())
        except:
            pass
        try:
            res = self.sockfd.recv(4096).decode()
        except:
            pass
        return res

    def close(self):
        self.sockfd.close()