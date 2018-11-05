#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : $register.py
# @Author: Hu
# @Date  : 2018.10
# @Contact：pinckhu@sina.com
from PyQt5.QtCore import Qt, pyqtSignal,QRegExp,QEvent,QPoint
from PyQt5.QtGui import QEnterEvent, QColor,QPixmap,QIcon,\
                        QPalette,QRegExpValidator,QCursor,\
                        QMouseEvent,QBrush
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel,\
                            QPushButton,QApplication,QLabel,\
                            QLineEdit,QWidget,QDesktopWidget,\
                            QMessageBox
from UI.mythread import MyThread,Mytthread
import hashlib
import image
import sys
import sip
'''
创建一个注册窗口的类
'''

class Register(QDialog):

    close_signal = pyqtSignal()

    def __init__(self,connfd,error):
        super(Register, self).__init__()
        self.connfd = connfd
        self.error = error
        self.timekey = False
        self.initUi()

    def initUi(self):
        self.setFixedSize(400, 200)                             # 创建固定窗口大小
        self.setWindowTitle('注册')                              # 窗口标题
        self.setWindowFlags(Qt.FramelessWindowHint)              # 无边框
        self.setWindowIcon(QIcon(':/logo.png'))
        window_pale = QPalette()                                 # 创建窗口背景图片对象
        window_pale.setBrush(self.backgroundRole(),\
                QBrush(QPixmap("UI/image/register.jpg"))) 
        self.setPalette(window_pale)

        pee = QPalette()                                          # 设置一个颜色
        pee.setColor(QPalette.WindowText,Qt.white)
        self.lbl_main = QLabel('注册', self)                       # 设置窗口名字
        self.lbl_main.move(10, 10)                                 #  窗口名的位置
        self.lbl_main.setPalette(pee)                              #窗口名的颜色

        pe = QPalette()                                           #设置字体颜色对象
        pe.setColor(QPalette.WindowText,Qt.gray)
        lucency = "background:transparent;\
                  border-width:0;border-style:outset"                             

        self.lbl_user = QLabel('账号:', self)                      # 创建一个标题用户名标题
        self.lbl_user.move(110, 36)
        self.lbl_user.setPalette(pe)

        self.Edit_user = QLineEdit(self)                           # 创建一个用户名输入框
        self.Edit_user.setGeometry(150, 27, 140, 30)               # 设置输入框的位置大小
        self.Edit_user.setPlaceholderText('手机号码')               # 悬浮显示提示信息
        self.Edit_user.setStyleSheet(lucency)                      # 透明输入框                            # 无边框设置
        self.Edit_user.setValidator(QRegExpValidator\
                    (QRegExp("[0-9]+"),self))                       # 限制用户输入信息的类型
        self.Edit_user.setMaxLength(11)                             # 输入框中的信息最大长度11
        self.Edit_user.setToolTip('用户名只能为11位的电话号码')       # 输入框的提示语句

        self.lbl_authcode = QLabel('验证:', self)                        # 创建一个标题昵称标题
        self.lbl_authcode.move(110, 66)
        self.lbl_authcode.setPalette(pe)

        self.Edit_authcode = QLineEdit(self)                            # 创建一个昵称输入框
        self.Edit_authcode.setGeometry(150, 57, 140, 30)                # 设置输入框的位置大小
        self.Edit_authcode.setPlaceholderText('输入验证码')                # 悬浮显示提示信息
        self.Edit_authcode.setStyleSheet(lucency)                        # 透明输入框                               # 无边框设置
        self.Edit_authcode.setValidator(QRegExpValidator\
                    (QRegExp("[0-9]+"),self))                           # 限制用户输入信息的类型
        self.Edit_authcode.setMaxLength(4)                              # 输入框中的信息最大长度11
        self.Edit_authcode.setToolTip('输入手机收到的4位数字验证码')                # 输入框的提示语句

        self.lbl_password = QLabel('密码:', self)                     # 创建密码标签
        self.lbl_password.move(110, 98)
        self.lbl_password.setPalette(pe)

        self.Edit_password = QLineEdit(self)                           # 创建密码输入框
        self.Edit_password.setGeometry(150, 89, 140, 30)
        self.Edit_password.setPlaceholderText('密码')
        self.Edit_password.setStyleSheet(lucency)
        self.Edit_password.setValidator(QRegExpValidator\
                            (QRegExp("[A-Za-z0-9]+"),self))
        self.Edit_password.setEchoMode(QLineEdit.Password)             #隐藏显示密码为圆点
        self.Edit_password.setMaxLength(16)
        self.Edit_password.setToolTip\
            ('用户密码最大长度为16位\n只能是大写字母、小写字母和数字')

        self.lbl_password2 = QLabel('确认:', self)                     # 创建确认密码标签
        self.lbl_password2.move(110, 130)
        self.lbl_password2.setPalette(pe)

        self.Edit_password2 = QLineEdit(self)                          # 创建密码输入框
        self.Edit_password2.setGeometry(150, 121, 140, 30)
        self.Edit_password2.setPlaceholderText('确认密码')
        self.Edit_password2.setStyleSheet(lucency)
        self.Edit_password2.setValidator(QRegExpValidator\
                            (QRegExp("[A-Za-z0-9]+"),self))
        self.Edit_password2.setEchoMode(QLineEdit.Password)              #隐藏显示密码为圆点
        self.Edit_password2.setMaxLength(16)
        self.Edit_password2.setToolTip('再次输入确认密码')
        
        color = "QPushButton{border:none;}"\
                "QPushButton:hover{border-image:\
                url(%s);border:none;}"

        self.button_register = QPushButton(' ', self)                    # 创建注册按钮
        self.button_register.setGeometry(87, 167, 230, 26)
        self.button_register.setStyleSheet(color % 'UI/image/register1.png')
        
        self.button_little = QPushButton(' ', self)                      # 创建最小化按钮
        self.button_little.setGeometry(336, 0, 32, 25)
        self.button_little.setToolTip('最小化')
        self.button_little.setStyleSheet(color % 'UI/image/login3.png')
        
        self.button_close = QPushButton(' ', self)                       # 创建关闭按钮
        self.button_close.setGeometry(368, 0, 32, 25)
        self.button_close.setToolTip('关闭')
        self.button_close.setStyleSheet(color % 'UI/image/login2.png')
        
        # 创建QWidget窗口对象
        self.centralwidget = QWidget(self)
        self.centralwidget.setGeometry(217, 51, 100, 40)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.sendauthcode()
        self.centralwidget0 = QWidget(self)                              # 创建一个QWidget窗口对象
        self.centralwidget0.setGeometry(317, 23, 100, 40)
        self.gridLayout0 = QGridLayout(self.centralwidget0)
        self.centralwidget1 = QWidget(self)
        self.centralwidget1.setGeometry(317, 51, 100, 40)
        self.gridLayout1 = QGridLayout(self.centralwidget1)
        self.centralwidget2 = QWidget(self)
        self.centralwidget2.setGeometry(317, 83, 100, 40)
        self.gridLayout2 = QGridLayout(self.centralwidget2)
        self.centralwidget3 = QWidget(self)
        self.centralwidget3.setGeometry(317, 116, 100, 40)
        self.gridLayout3 = QGridLayout(self.centralwidget3)

        self.button_little.clicked.connect(self.showMinimized)            # 按键事件
        self.button_register.clicked.connect(self.onregister)

        # 定义获取焦点事件
        self.Edit_user.installEventFilter(self)                            # 定义获取焦点事件
        self.Edit_authcode.installEventFilter(self)
        self.Edit_password.installEventFilter(self)
        self.Edit_password2.installEventFilter(self)
    
    # 创建一个发送验证的按键
    def sendauthcode(self,show='发送验证码'):
        color = "QPushButton{border:none;color:rgb(0, 0, 0);}"\
                "QPushButton:hover{border:none;color:rgb(255, 186, 0);}"
        self.Button_sendauthcode = QPushButton(show,self.centralwidget)
        self.Button_sendauthcode.setStyleSheet(color)
        self.gridLayout.addWidget(self.Button_sendauthcode, 0, 0, 1, 1)
        self.Button_sendauthcode.clicked.connect(self.send_authcode)
        QApplication.processEvents()
    
    def send_authcode(self):
        # 先要验证数据库有没有这个账号
        user = self.Edit_user.text()
        if not user:
            self.user_Error_hint('*账号不为空')
            return
        try:    
            if user[0] != '1' or user[1] in ['0', '1', '2'] or len(user) < 11:
                self.user_Error_hint('*不是手机号')
                return
        except IndexError:
            self.user_Error_hint('*不是手机号')
            return
        data = 'VV ' + user
        self.threadmess = MyThread(self.connfd,data)
        self.threadmess.messageSignal.connect(self.handle_return_authcode)
        self.threadmess.start()
    
    # 处理验证发送返回的消息
    def handle_return_authcode(self,mess):
        self.threadmess.deleteLater()
        if mess == 'VVNO NotUser':
            self.user_Error_hint('*账号已存在')
            return 
        elif mess == 'VVOK ':
            self.authcode_Error_hint('*发送成功')
        # 创建线程
        self.mthread = Mytthread()
        # 注册信号处理函数
        self.mthread.breakSignal.connect(self.handle_authcode)
        # 启动线程
        self.mthread.start()
    
    # 多线程处理
    def handle_authcode(self,i):
        if i == 60:
            self.Button_sendauthcode.setStyleSheet\
                ("QPushButton{border:none;color:rgb(200, 200, 200);}")
            self.Button_sendauthcode.setEnabled(False)
        elif i == 0:
            self.Button_sendauthcode.setEnabled(True)
            self.Button_sendauthcode.setText('发送验证码')
            self.Button_sendauthcode.setStyleSheet\
                ("QPushButton{border:none;color:rgb(0, 0, 0);}")
            return
        self.Button_sendauthcode.setText('%s秒后可重发'%i)

    # 定义获取焦点事件处理
    def eventFilter(self, obj, event):
        if obj == self.Edit_user:
            if event.type()== QEvent.FocusIn:
                self.user_Error_hint()
            return False
        elif obj == self.Edit_authcode:
            if event.type()== QEvent.FocusIn:
                self.authcode_Error_hint()
            return False
        elif obj == self.Edit_password:
            if event.type()== QEvent.FocusIn:
                self.password_Error_hint()
            return False
        elif obj == self.Edit_password2:
            if event.type()== QEvent.FocusIn:
                self.password_Error_hint2()
            return False
    
    # 处理注册按键事件
    def onregister(self):
        if self.error == 'NetworkConnectIonisFailed':
            self.user_Error_hint('*网络错误')
            self.authcode_Error_hint('*网络错误')
            self.password_Error_hint('*网络错误')
            self.password_Error_hint2('*网络错误')
            return
        user = self.Edit_user.text()
        authcode = self.Edit_authcode.text()
        password = self.Edit_password.text()
        password2 = self.Edit_password2.text()
        if len(user) < 11:
            self.user_Error_hint('*账号错误')
            return
        elif len(authcode) < 4:
            self.authcode_Error_hint('*验证码错误')
            return
        elif not password:
            self.password_Error_hint('*不能为空')
            return
        elif not password2:
            self.password_Error_hint2('*不能为空')
            return
        elif len(password) < 6:
            self.password_Error_hint('*密码至少6位')
            return
        elif password != password2:
            self.password_Error_hint2('*密码不一致')
            return
        if self.timekey:
            return
        # 让这个变量为True
        self.timekey = True
        password = hashlib.md5(self.Edit_password.text().\
                    encode(encoding='UTF-8')).hexdigest()
        data = 'R ' + user + ' ' + authcode + ' ' + password
        self.threadmess = MyThread(self.connfd,data)
        self.threadmess.messageSignal.connect(self.handle_return_message)
        self.threadmess.start()
    
    # 处理注册返回的情况处理
    def handle_return_message(self,mess):
        self.threadmess.deleteLater()
        if mess == 'RNO UserRepeat':
            self.user_Error_hint('*账号已存在')
        elif mess == 'RNO TheVerificationVodeIsNotCorrect':
            self.authcode_Error_hint('*验证码错误')
        elif mess == 'ROK ':
            self.hide()
            self.handle_click()
            self.user_Error_hint('*注册成功')
        elif mess == 'RNO RegistrationFailed':
            self.user_Error_hint('*注册失败')
        # 把按键检测变为False
        self.timekey = False

    #处理显示账号错误信息
    def user_Error_hint(self,show=' '):
        try:
            sip.delete(self.name_hint)
        except AttributeError:
            pass
        pe_red = QPalette()
        pe_red.setColor(QPalette.WindowText,Qt.red)
        self.name_hint = QLabel(show,self.centralwidget0)
        self.name_hint.setPalette(pe_red)
        self.gridLayout0.addWidget(self.name_hint, 0, 0, 1, 1)
        QApplication.processEvents()
    
    # 验证码错误显示内容处理
    def authcode_Error_hint(self,show=' '):
        try:
            sip.delete(self.authcode_hint)
        except AttributeError:
            pass
        pe_red = QPalette()
        pe_red.setColor(QPalette.WindowText,Qt.red)
        self.authcode_hint = QLabel(show,self.centralwidget1)
        self.authcode_hint.setPalette(pe_red)
        self.gridLayout1.addWidget(self.authcode_hint, 0, 0, 1, 1)
        QApplication.processEvents()
        
    #处理显示密码错误信息
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
    
    #处理显示确认密码显示错误信息
    def password_Error_hint2(self,show=' '):
        try:
            sip.delete(self.password_hint2)
        except AttributeError:
            pass
        pe_red = QPalette()
        pe_red.setColor(QPalette.WindowText,Qt.red)
        self.password_hint2 = QLabel(show,self.centralwidget3)
        self.password_hint2.setPalette(pe_red)
        self.gridLayout3.addWidget(self.password_hint2, 0, 0, 1, 1)
        QApplication.processEvents()

    # 对ESC进行的重载  按ESC也有退出的功能
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
            self.close_signal.emit()

    #  把隐藏的窗口显示出来
    def handle_click(self):
        if not self.isVisible():
            self.Edit_user.clear()
            self.Edit_authcode.clear()
            self.Edit_password.clear()
            self.Edit_password2.clear()
            self.show()

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