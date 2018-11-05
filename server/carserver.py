#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : $carserver.py
# @Author : Fire organize
# @Date   : 2018.10
# @Contact：xxxx

from threading import Thread
from handlemessage import HandleMessage
from handlesql import HandleSql
from zhenzismsclient import ZhenziSmsClient
from socket import *


class CarServer(object):
    '''
    这是一个货运信息平台通信的服务器的类
    '''
    def __init__(self,addr = ('',1080)):
        # 使用的是TCP类型
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.addr = addr
        self.sockfd.bind(self.addr)
        self.handle_sql = HandleSql()
    
    #启动服务器
    def serve_forever(self):
        self.sockfd.listen(10)
        print('服务器启动，等待连接对象')
        while True:
            connfd,addr = self.sockfd.accept()
            print('有客户端连接到服务器',addr)
            # 使用多线程处理客户端的请求和响应
            handle_client = Thread\
                (target = self.handle_request,args = (connfd,))
            handle_client.setDaemon(True)
            handle_client.start()
    
    # 处理客户端请求
    def handle_request(self,connfd):
        client = ZhenziSmsClient('http://sms_developer.zhenzikj.com',\
             '100040', 'MGRhYzE4YWUtYWY2OC00Y2UwLTg1ZDItZjc5ZTM0NjNjM2Vi')
        handlemessage = HandleMessage(self.handle_sql,client)
        while True:
            try:
                data = connfd.recv(4096).decode()
            except:
                connfd.close()
                break
            if not data:
                connfd.close()
                break
            res = handlemessage.request_type(data)
            try:
                connfd.send(res.encode())
            except AttributeError:
                connfd.close()
                break


if __name__ == '__main__':
    CarServer = CarServer()
    CarServer.serve_forever()