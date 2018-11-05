#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : $Guimain.py
# @Author: Hu
# @Date  : 2018.10
# @Contact：pinckhu@sina.com
'''
此程序是处理每个窗口跳转的逻辑程序
'''
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication
from communication import MySocket
from UI.login import Login
from UI.register import Register
from UI.lose import Lose
from UI.mainui import MainWindow
from UI.newmessage import NewMessage
from UI.mymessage import MyMessage
from UI.altermessage import AlterMessage
from UI.alter import Alter
import sys

error = 'normal'
try:
    mymess = MySocket()
except:
    mymess = None
    error = 'NetworkConnectIonisFailed'

def Guimain():
    app = QApplication(sys.argv)
    login = Login(mymess,error)
    register = Register(mymess,error)
    lose = Lose(mymess,error)

    # 关闭login窗口把当前窗口的位置传给register窗口
    def handle_size_login_register():
        rect = login.geometry()
        register.handle_size(rect.left(), rect.top())
    
    # 关闭register窗口把当前窗口的位置传给loginr窗口
    def handle_size_register_login():
        rect = register.geometry()
        login.handle_size(rect.left(), rect.top())

    # 关闭login窗口把当前窗口的位置传给lose 窗口
    def handle_size_login_lose():
        rect = login.geometry()
        lose.handle_size(rect.left(), rect.top())
    
    # 关闭lose 窗口把当前窗口的位置传给logi窗口
    def handle_size_lose_login():
        rect = lose.geometry()
        login.handle_size(rect.left(), rect.top())

    # login的button_register按键处理的事件
    login.button_register.clicked.connect(register.handle_click)
    login.button_register.clicked.connect(handle_size_login_register)
    login.button_register.clicked.connect(login.hide)


    register.button_close.clicked.connect(login.handle_click)
    register.button_close.clicked.connect(handle_size_register_login)
    register.button_close.clicked.connect(register.hide)
    register.close_signal.connect(login.handle_click)
    register.close_signal.connect(handle_size_register_login)

    # login的button_lose按键处理的事件
    login.button_lose.clicked.connect(lose.handle_click)
    login.button_lose.clicked.connect(handle_size_login_lose)
    login.button_lose.clicked.connect(login.hide)

    lose.button_close.clicked.connect(login.handle_click)
    lose.button_close.clicked.connect(handle_size_lose_login)
    lose.button_close.clicked.connect(lose.hide)
    lose.close_signal.connect(login.handle_click)
    lose.close_signal.connect(handle_size_lose_login)

    # login 按钮事件处理
    def handle_button_login():
        # 执行登录验证
        login.onlogin()
    
    # 验证账号密码成功后执行登录主页面操作
    def login_succeed(user):
        if user:
            # 关闭login窗口把当前窗口的位置传给mainui 窗口
            def handle_size_login_mainui():
                rect = login.geometry()
                mainui.handle_size(rect.left() - 312, rect.top() - 260)
    
            # 关闭mainui 窗口把当前窗口的位置传给login窗口
            def handle_size_mainui_login():
                rect = mainui.geometry()
                login.handle_size(rect.left() + 312, rect.top() + 260)
            
            # 执行打开newmessage窗口
            def handle_button_newmessage():
                # 关闭mainui窗口把当前窗口的位置传给newmessage窗口
                def handle_size_mainui_newmwssage():
                    rect = mainui.geometry()
                    newmessage.handle_size(rect.left() + 244, rect.top() + 60)
        
                # 关闭newmessage窗口把当前窗口的位置传给mainui窗口
                def handle_size_newmessage_mainui():
                    rect = newmessage.geometry()
                    mainui.handle_size(rect.left() - 244, rect.top() - 60)

                mainui.hide()
                newmessage = NewMessage(user,mymess)
                newmessage.handle_click()
                handle_size_mainui_newmwssage()

                newmessage.button_close.clicked.connect(mainui.handle_click)
                newmessage.button_close.clicked.connect(handle_size_newmessage_mainui)
                newmessage.button_close.clicked.connect(newmessage.close)
                newmessage.close_signal.connect(mainui.handle_click)
                newmessage.close_signal.connect(handle_size_newmessage_mainui)
            
            # 执行打开mymessage窗口
            def handle_button_mymessage():
                # 关闭mainui窗口把当前窗口的位置传给mymessage窗口
                def handle_size_mainui_mymessage():
                    rect = mainui.geometry()
                    mymessage.handle_size(rect.left() + 244, rect.top() + 60)
        
                # 关闭newmessage窗口把当前窗口的位置传给mainui窗口
                def handle_size_mymessage_mainui():
                    rect = mymessage.geometry()
                    mainui.handle_size(rect.left() - 244, rect.top() - 60)
                
                # 打开一个编辑页面
                def handle_signal_alter(mess):
                    # 关闭mymessage窗口把当前窗口的位置传给altermessage窗口
                    def handle_size_mymessage_altermessage():
                        rect = mymessage.geometry()
                        altermessage.handle_size(rect.left() - 45, rect.top() - 110)
            
                    # 关闭altermessage窗口把当前窗口的位置传给mymessage窗口
                    def handle_size_altermessage_mymessage():
                        rect = altermessage.geometry()
                        mymessage.handle_size(rect.left() + 45, rect.top() + 110)

                    mymessage.hide()
                    altermessage = AlterMessage(mess,mymess)
                    altermessage.handle_click()
                    handle_size_mymessage_altermessage()

                    altermessage.button_close.clicked.connect(mymessage.handle_click)
                    altermessage.button_close.clicked.connect\
                                        (handle_size_altermessage_mymessage)
                    altermessage.button_close.clicked.connect(altermessage.close)
                    altermessage.close_signal.connect(mymessage.handle_click)
                    altermessage.close_signal.connect\
                                        (handle_size_altermessage_mymessage)

                mymessage = MyMessage(user,mymess)
                mymessage.handle_click()
                handle_size_mainui_mymessage()
                mainui.hide()

                mymessage.button_close.clicked.connect(mainui.handle_click)
                mymessage.button_close.clicked.connect(handle_size_mymessage_mainui)
                mymessage.button_close.clicked.connect(mymessage.close)
                mymessage.close_signal.connect(mainui.handle_click)
                mymessage.close_signal.connect(handle_size_mymessage_mainui)
                mymessage.altermess.connect(handle_signal_alter)
            
            # 执行打开alter窗口
            def handle_button_alter():
                # 关闭mainui窗口把当前窗口的位置传给alter窗口
                def handle_size_mainui_alter():
                    rect = mainui.geometry()
                    alter.handle_size(rect.left() + 213, rect.top() + 260)
        
                # 关闭newmessage窗口把当前窗口的位置传给mainui窗口
                def handle_size_alter_mainui():
                    rect = alter.geometry()
                    mainui.handle_size(rect.left() - 312, rect.top() -260)

                alter = Alter(user,mymess)
                alter.handle_click()
                handle_size_mainui_alter()
                mainui.hide()

                alter.button_close.clicked.connect(mainui.handle_click)
                alter.button_close.clicked.connect(handle_size_alter_mainui)
                alter.button_close.clicked.connect(alter.close)
                alter.close_signal.connect(mainui.handle_click)
                alter.close_signal.connect(handle_size_alter_mainui)
            
            mainui = MainWindow(user,mymess)
            mainui.handle_click()
            handle_size_login_mainui()
            login.hide()

            mainui.logoutSignal.connect(login.handle_click)
            mainui.button_user.clicked.connect(handle_size_mainui_login)
            mainui.button_user.clicked.connect(mainui.close)

            mainui.button_newmessage.clicked.connect(handle_button_newmessage)
            mainui.button_mymessage.clicked.connect(handle_button_mymessage)
            mainui.button_data.clicked.connect(handle_button_alter)
    
    # login的button_lose按键处理的事件
    login.button_login.clicked.connect(handle_button_login)
    # 验证账号密码成功后的信号
    login.loginSignal.connect(login_succeed)

    login.show()
    sys.exit(app.exec_())