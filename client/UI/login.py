#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : $login.py
# @Author : Hu
# @Date   : 2018.10
# @Contact：pinckhu@sina.com

from PyQt5.QtCore import Qt, pyqtSignal,QRegExp,QEvent,QPoint
from PyQt5.QtGui import QEnterEvent, QColor,QPixmap,QIcon,\
                        QPalette,QRegExpValidator,QCursor,\
                        QMouseEvent,QBrush
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel,\
                            QPushButton,QApplication,QLabel,\
                            QLineEdit,QWidget,QDesktopWidget,\
                            QMessageBox
from UI.mythread import MyThread
import hashlib
import image
import sys
import sip
'''
创建一个登陆窗口的类
'''

class Login(QDialog):

    loginSignal = pyqtSignal(str)

    def __init__(self,connfd,error):
        super(Login, self).__init__()
        self.connfd = connfd
        self.error = error
        self.timekey = False
        self.initUi()

    def initUi(self):
        self.setFixedSize(400, 200)                      # 创建固定窗口大小         # 窗口标题
        self.setWindowFlags(Qt.FramelessWindowHint)      # 设置窗口无边框
        self.setWindowIcon(QIcon(':/logo.png')) 

        window_pale = QPalette()                           # 创建窗口背景图片对象
        window_pale.setBrush(self.backgroundRole(),\
                QBrush(QPixmap("UI/image/login.jpg")))        # 按指定路径找到图片
        self.setPalette(window_pale)

        pee = QPalette()                                  # 设置程序显示名的颜色
        pee.setColor(QPalette.WindowText,Qt.white)
        colo = QPalette()                                    #设置普通文字的颜色
        colo.setColor(QPalette.WindowText,Qt.red)
        
        if self.error == 'normal':
            self.lbl_main = QLabel('货运信息公共平台', self)    #设置程序的名字
            self.lbl_main.setPalette(pee)
        elif self.error == 'NetworkConnectIonisFailed':
            self.lbl_main = QLabel('*网络连接失败*', self)    #设置程序的名字
            self.lbl_main.setPalette(colo)
        self.lbl_main.move(10, 10)

        pe = QPalette()                                    #设置普通文字的颜色
        pe.setColor(QPalette.WindowText,Qt.gray)
        lucency = "background:transparent;border-width:\
                0;border-style:outset"

        self.lbl_user = QLabel('账号:', self)                 # 创建一个标题用户名标题
        self.lbl_user.move(110, 55)
        self.lbl_user.setPalette(pe)
        
        self.Edit_user = QLineEdit(self)                       # 创建一个用户名输入框对象
        self.Edit_user.setGeometry(150, 45, 140, 30)           # 设置输入框的位置大小
        self.Edit_user.setPlaceholderText('手机号码')           # 悬浮显示提示信息
        self.Edit_user.setStyleSheet(lucency)                  # 透明输入框                      # 无边框设置
        self.Edit_user.setValidator(QRegExpValidator\
                    (QRegExp("[0-9]+"),self))                  # 限制用户输入信息的类型
        self.Edit_user.setMaxLength(11)                        # 输入框中的信息最大长度11
        self.Edit_user.setToolTip('用户名只能为11位的电话号码')  # 输入框的提示语句
        
        self.lbl_password = QLabel('密码:', self)               # 创建密码标签
        self.lbl_password.move(110, 90)
        self.lbl_password.setPalette(pe)

        self.Edit_password = QLineEdit(self)                   # 创建密码输入框
        self.Edit_password.setGeometry(150, 80, 140, 30)
        self.Edit_password.setPlaceholderText('密码')
        self.Edit_password.setStyleSheet(lucency)
        self.Edit_password.setValidator(QRegExpValidator\
                            (QRegExp("[A-Za-z0-9]+"),self))
        self.Edit_password.setEchoMode(QLineEdit.Password)     #隐藏显示密码为圆点
        self.Edit_password.setMaxLength(16)
        self.Edit_password.setToolTip('用户密码最大长度为16位')
        
        # 设置按键背景和悬停的属性变量
        color = "QPushButton{border:none;color:rgb(55, 255, 255);}"\
            "QPushButton:hover{border:none;color:rgb(255, 255, 255);}"
        color2 = "QPushButton{border:none;}"\
                "QPushButton:hover{border-image:\
                url(%s);border:none;}"

        self.button_register = QPushButton('注册', self)      # 创建注册按钮对象
        self.button_register.setGeometry(76, 160, 70, 28)
        self.button_register.setStyleSheet(color)             # 给按钮添加属性

        self.button_lose = QPushButton('忘记密码', self)       # 创建忘记密码按钮对象
        self.button_lose.setGeometry(250, 160, 70, 28)
        self.button_lose.setStyleSheet(color)

        self.button_login = QPushButton(' ', self)             # 创建登陆按钮对象
        self.button_login.setGeometry(88, 130, 230, 26)
        self.button_login.setStyleSheet(color2 % 'UI/image/login1.png')
        
        self.button_little = QPushButton(' ', self)            # 创建最小化按钮对象
        self.button_little.setGeometry(336, 0, 32, 25)
        self.button_little.setToolTip('最小化')
        self.button_little.setStyleSheet(color2 % 'UI/image/login3.png')
        
        self.button_close = QPushButton(' ', self)             # 创建关闭按钮对象
        self.button_close.setGeometry(368, 0, 32, 25)
        self.button_close.setToolTip('关闭')
        self.button_close.setStyleSheet(color2 % 'UI/image/login2.png')
        
        self.centralwidget = QWidget(self)                     # 创建一个QWidget窗口对象
        self.centralwidget.setGeometry(317, 40, 100, 40)       # 设置对象的大小位置
        self.gridLayout = QGridLayout(self.centralwidget)      # 在self.centralwidget窗口中添加一个布局
        self.centralwidget2 = QWidget(self)
        self.centralwidget2.setGeometry(317, 76, 100, 40)
        self.gridLayout2 = QGridLayout(self.centralwidget2)
        
        screen = self.frameGeometry()                           # 窗口居中显示
        wall = QDesktopWidget().availableGeometry().center()
        screen.moveCenter(wall)
        self.move(screen.topLeft())

        self.button_little.clicked.connect(self.showMinimized)   # 为按键添加信号事件
        self.button_close.clicked.connect(self.close_quit)
    
        self.Edit_user.installEventFilter(self)                  # 定义对象获取焦点事件
        self.Edit_password.installEventFilter(self)

    # 定义获取焦点事件处理方法
    def eventFilter(self, obj, event):
        if obj == self.Edit_user:
            if event.type()== QEvent.FocusIn:
                self.user_Error_hint()
            return False
        elif obj == self.Edit_password:
            if event.type()== QEvent.FocusIn:
                self.password_Error_hint()
            return False
    
    #定义self.centralwidget窗口中的事件处理方法
    def user_Error_hint(self,show=' '):
        try:
            sip.delete(self.user_hint)
        except AttributeError:
            pass
        pe_red = QPalette()
        pe_red.setColor(QPalette.WindowText,Qt.red)
        self.user_hint = QLabel(show,self.centralwidget)
        self.user_hint.setPalette(pe_red)
        self.gridLayout.addWidget(self.user_hint, 0, 0, 1, 1)
        QApplication.processEvents()
    
    #定义self.centralwidget2窗口中的事件处理方法
    def password_Error_hint(self,show=' '):
        try:
            sip.delete(self.password_hint)
        except AttributeError:
            pass
        pe_red = QPalette()
        pe_red.setColor(QPalette.WindowText,Qt.red)
        self.password_hint = QLabel(show,self.centralwidget2)
        self.password_hint.setPalette(pe_red)
        self.gridLayout2.addWidget(self.password_hint, 0, 0, 1, 1)
        QApplication.processEvents()
    
    # 重写无边框拖动方法
    def mouseMoveEvent(self, e: QMouseEvent):
        try:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)
        except TypeError:
            pass

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    # 处理登录按钮事件的逻辑
    def onlogin(self):
        self.user = self.Edit_user.text()  
        password = self.Edit_password.text()
        if not self.user:
            self.user_Error_hint('*不能为空')
            return
        elif len(self.user) < 11:
            self.user_Error_hint('*账号错误')
            return
        elif not password:
            self.password_Error_hint('*不能为空')
            return
        elif len(password) < 6:
            self.password_Error_hint('*小于6位')
            return
        password = hashlib.md5(self.Edit_password.text().\
                    encode(encoding='UTF-8')).hexdigest()
        data = 'L ' + self.user + ' ' + password
        # 如果这个变量为True直接退出
        if self.timekey:
            return
        # 如果网络没有连接上的情况
        if self.error == 'NetworkConnectIonisFailed':
            self.user_Error_hint('*网络错误')
            self.password_Error_hint('*网络错误')
            return
        # 让这个变量为True
        self.timekey = True
        self.threadmess = MyThread(self.connfd,data)
        self.threadmess.messageSignal.connect(self.handle_return_message)
        self.threadmess.start()
    
    # 处理登录返回的情况处理
    def handle_return_message(self,mess):
        self.threadmess.deleteLater()
        if mess == 'LNO NotUser':
            self.user_Error_hint('*账号不存在')
        elif mess == 'LNO PasswordError':
            self.password_Error_hint('*密码错误')
        elif mess == 'LOK ':
            self.loginSignal.emit(self.user)
        # 把按键检测变为False
        self.timekey = False

    # 其他窗口关闭跳转到此窗口时的位置重载
    def handle_size(self, left, top):
        screen = self.frameGeometry()                                   # 窗口显示位置
        wall = QDesktopWidget().availableGeometry().center()
        screen.moveCenter(wall)
        if left < 0:
            left = 0
        if top < 0:
            top = 0
        if left > screen.left() * 2:
            left = screen.left() * 2
        if top > screen.top() * 2:
            top = screen.top() * 2
        self.move(left, top)
        QApplication.processEvents()
    
    # 把隐藏的窗口显示出来
    def handle_click(self):
        if not self.isVisible():
            self.Edit_user.clear()
            self.Edit_password.clear()
            self.show()
    
    # 对关闭重写
    def close_quit(self):
        try:
            self.connfd.close()
        except AttributeError:
            pass
        self.close()# 

    # 对ESC进行的重载  按ESC也有退出的功能
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close_quit()