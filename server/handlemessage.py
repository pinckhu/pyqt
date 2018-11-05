#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : $carserver.py
# @Author : Fire organize
# @Date   : 2018.10
# @Contact：xxxx

import random


class HandleMessage(object):
    '''
    这是一个对客户端请求的分析和做出相应的结果的类
    '''
    def __init__(self, handlesql,client):
        # 创建一个对数据库交互的对象
        self.handle_sql = handlesql
        self.client = client
        self.verificationcode = 10000
        self.publish_message = ''
    
    # 分析请求类型
    def request_type(self,content):
        request = content.split(' ')
        retype = request[0]
        if retype == 'L':
            return self.handle_login(request[1],request[2])
        elif retype == 'R':
            return self.handle_register(request[1],request[2],request[3])
        elif retype == 'V':
            return self.handle_verify(request[1])
        elif retype == 'VV':
            return self.handle_vverify(request[1])
        elif retype == 'P':
            return self.handle_lose(request[1],request[2],request[3])
        elif retype == 'N':
            return self.handle_password(request[1],request[2],request[3])
        elif retype == 'H':
            return self.handle_catalogue(request[1],request[2],request[3])
        elif retype == 'M':
            return self.handle_history(request[1])
        elif retype == 'X':
            return self.handle_detail(request[1],request[2])
        elif retype == 'F':
            return self.handle_publish(request[1],request[2])
        elif retype == 'C':
            return self.handle_mypublish(request[1],request[2])
        elif retype == 'U':
            return self.handle_compile(request[1])
        elif retype == 'UX':
            return self.handle_save_compile(request[1],request[2])
        else:
            pass

    # 对登录进行处理
    def handle_login(self,user,password):
        res = self.handle_sql.handle_user(user)
        if res == None:
            return 'LNO NotUser'
        elif res[0] == password:
            return 'LOK '
        return 'LNO PasswordError'

    # 对注册进行处理
    def handle_register(self,user,authcode,password):
        # 验证码不正确
        if self.verificationcode != int(authcode):
            return 'RNO TheVerificationVodeIsNotCorrect'
        res = self.handle_sql.handle_user(user)
        if res == None:
            ress = self.handle_sql.handle_register(user,password)
            if ress == 'NO':
                return 'RNO RegistrationFailed'
            return 'ROK '
        return 'RNO UserRepeat'
        self.verificationcode = 10000

    # 对验证手机号码处理
    def handle_verify(self,user):
        res = self.handle_sql.handle_user(user)
        if res == None:
            return 'VNO NotUser'
        self.verificationcode = random.randrange(1000,9999)
        # 实现验证码发送成功
        result = self.client.send(user, '欢迎使用【货运信息公共平台】服务,您的验证码为' \
            + str(self.verificationcode) + ',如非本人操作请注意账号安全,本次验证码10分钟内有效!')
        if result == '{"code":0,"data":"发送成功"}':
            return 'VOK '
        return 'VNO BeDefeated'
    
    # 对注册验证手机号码处理
    def handle_vverify(self,user):
        res = self.handle_sql.handle_user(user)
        if res:
            return 'VVNO NotUser'
        self.verificationcode = random.randrange(1000,9999)
        # 实现验证码发送成功
        result = self.client.send(user, '欢迎使用【货运信息公共平台】服务,您的验证码为' \
            + str(self.verificationcode) + ',如非本人操作请注意账号安全,本次验证码10分钟内有效!')
        if result == '{"code":0,"data":"发送成功"}':
            return 'VVOK '
        return 'VVNO BeDefeated'
    
    # 对找回的新密码进行处理
    def handle_lose(self,user,authcode,password):
        # 验证码不正确
        if self.verificationcode != int(authcode):
            return 'PNO TheVerificationVodeIsNotCorrect'
        res = self.handle_sql.handle_user(user)
        if res == None:
            return 'PNO NotUser'
        elif res[0] == password:
            return 'PNO PasswordRepetition'
        ress = self.handle_sql.handle_password(user,password)
        if ress == 'NO':
            return 'PNO Bedefeated'
        self.verificationcode = 10000
        return 'POK '

    # 对修改密码进行处理
    def handle_password(self,user,ypassword,password):
        res = self.handle_sql.handle_user(user)
        if res[0] != ypassword:
            return 'NNO PasswordRepetition'
        ress = self.handle_sql.handle_password(user,password)
        if ress == 'NO':
            return 'NNO Bedefeated'
        return 'NOK '
    
    # 对主窗口的货运目录进行处理
    def handle_catalogue(self,origin,goal,page):
        res = self.handle_sql.handle_catalogue(origin,goal,page)
        if res == ():
            return 'HFNO NoData'
        ress = 'HF '
        for i in res:
            l = [str(a) for a in i]
            ress += '#'.join(l)
            ress += ' '
        # 返回的字符串类型'HF 起点市 起点县 终点市 终点县 浏览时间'
        return ress[:len(ress)-1]

    # 对用户浏览记录进行处理
    def handle_history(self,user):
        res = self.handle_sql.handle_history(user)
        if res == 'NO':
            return 'MFNO NoData'
        # 返回的字符串类型'MF 起点市 起点县 终点市 终点县 浏览时间'
        return res
    
    # 对用户请求详细信息进行处理
    def handle_detail(self,user,id):
        res = self.handle_sql.handle_detail(user,id)
        ress = 'XF '
        l = [str(res[i]) for i in range(len(res)) if i!=0 or i!=1]
        return ress + '#'.join(l)

    # 对发布一条信息进行处理
    def handle_publish(self,user,message):
        res = self.handle_sql.handle_publish(user,message)
        if res == 'NO':
            return 'FFNO NoData'
        self.publish_message = message
        return 'FFOK '
    
    # 对用户发布过信息目录进行处理
    def handle_mypublish(self,user,page):
        res = self.handle_sql.handle_mypublish(user,page)
        if res == 'NO':
            return 'CFNO NoData'
        ress = 'CF '
        for i in res:
            l = [str(a) for a in i]
            ress += '#'.join(l)
            ress += ' '
        return ress[:len(ress)-1]
    
    # 编辑相应ID的信息
    def handle_compile(self,id):
        res = self.handle_sql.handle_compile(id)
        if res == 'NO':
            return 'UFNO NoData'
        ress = 'UF '
        l = [str(res[i]) for i in range(len(res)) if i!=1]
        return  ress + '#'.join(l)
    # 保存编辑相应ID的信息
    def handle_save_compile(self,id,message):
        res = self.handle_sql.handle_save_compile(id,message)
        if res == 'NO':
            return 'UXNO NoData'
        return 'UXOK '