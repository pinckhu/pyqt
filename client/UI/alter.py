#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : $alter.py
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


class Alter(QDialog):

    close_signal = pyqtSignal()

    def __init__(self,user,connfd):
        super(Alter, self).__init__()
        self.connfd = connfd
        self.user = user
        self.timekey = False
        self.initUi()

    def initUi(self):
        # 创建固定窗口大小
        self.setFixedSize(400, 200)
        # 窗口标题
        self.setWindowTitle('修改窗口')
        # 无边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(':/logo.png'))

        window_pale = QPalette()
        window_pale.setBrush(self.backgroundRole(),\
                QBrush(QPixmap("UI/image/alter.jpg"))) 
        self.setPalette(window_pale)

        # 程序名
        pee = QPalette()
        pee.setColor(QPalette.WindowText,Qt.white)
        self.lbl_main = QLabel('修改资料', self)
        self.lbl_main.move(10, 10)
        self.lbl_main.setPalette(pee)

        #设置字体颜色
        pe = QPalette()
        pe.setColor(QPalette.WindowText,Qt.gray)

        # 创建一个标题用户名标题
        self.lbl_user = QLabel('账号:', self)
        self.lbl_user.move(110, 36)
        self.lbl_user.setPalette(pe)
        
        # 创建一个用户名输入框
        self.Edit_user = QLineEdit(self)
        self.Edit_user.setReadOnly(True)                       # 输入框不能修改
        self.Edit_user.setGeometry(150, 27, 140, 30)           # 设置输入框的位置大小
        self.Edit_user.setPlaceholderText(self.user)           # 悬浮显示提示信息
        self.Edit_user.setStyleSheet("background:\
            transparent;border-width:0;border-style:outset")   # 透明输入框   

        # 创建一个标题昵称标题
        self.lbl_name = QLabel('旧密:', self)
        self.lbl_name.move(110, 66)
        self.lbl_name.setPalette(pe)

        # 创建一个昵称输入框
        self.Edit_name = QLineEdit(self)
        self.Edit_name.setGeometry(150, 57, 140, 30)           # 设置输入框的位置大小
        self.Edit_name.setPlaceholderText('输入旧密码')           # 悬浮显示提示信息
        self.Edit_name.setStyleSheet("background:\
            transparent;border-width:0;border-style:outset")   # 透明输入框                        # 无边框设置
        self.Edit_name.setValidator(QRegExpValidator\
                    (QRegExp("[A-Za-z0-9]+"),self))                      # 限制用户输入信息的类型
        self.Edit_name.setMaxLength(16)                        # 输入框中的信息最大长度11
        self.Edit_name.setEchoMode(QLineEdit.Password) 
        self.Edit_name.setToolTip\
            ('单独修改昵称,密码栏为空\n同时修改都填入新昵称')                 # 输入框的提示语句
        
        # 创建密码标签
        self.lbl_password = QLabel('新密:', self)
        self.lbl_password.move(110, 98)
        self.lbl_password.setPalette(pe)

        # 创建密码输入框
        self.Edit_password = QLineEdit(self)
        self.Edit_password.setGeometry(150, 89, 140, 30)
        self.Edit_password.setPlaceholderText('输入新密码')
        self.Edit_password.setStyleSheet("background:\
            transparent;border-width:0;border-style:outset")
        self.Edit_password.setValidator(QRegExpValidator\
                                    (QRegExp("[A-Za-z0-9]+"),self))
        self.Edit_password.setEchoMode(QLineEdit.Password)     #隐藏显示密码为圆点
        self.Edit_password.setMaxLength(16)
        self.Edit_password.setToolTip('用户密码最大长度为16位')

        # 创建确认密码标签
        self.lbl_password2 = QLabel('确认:', self)
        self.lbl_password2.move(110, 130)
        self.lbl_password2.setPalette(pe)

        # 创建密码输入框
        self.Edit_password2 = QLineEdit(self)
        self.Edit_password2.setGeometry(150, 121, 140, 30)
        self.Edit_password2.setPlaceholderText('确认密码')
        self.Edit_password2.setStyleSheet("background:\
            transparent;border-width:0;border-style:outset")
        self.Edit_password2.setValidator(QRegExpValidator\
                                (QRegExp("[A-Za-z0-9]+"),self))
        self.Edit_password2.setEchoMode(QLineEdit.Password)     #隐藏显示密码为圆点
        self.Edit_password2.setMaxLength(16)
        self.Edit_password2.setToolTip('用户密码最大长度为16位')

        color = "QPushButton{;border:none;color:rgb(55, 255, 255);}"\
                "QPushButton:hover{border-image: url(%s);\
                border:none;color:rgb(255, 255, 255);}"
        
        # 创建按钮
        self.button_alter = QPushButton(' ', self)
        self.button_alter.setGeometry(87, 167, 230, 26)
        self.button_alter.setStyleSheet(color % "UI/image/alter1.png")
        
        self.button_little = QPushButton(' ', self)
        self.button_little.setGeometry(336, 0, 32, 25)
        self.button_little.setToolTip('最小化')
        self.button_little.setStyleSheet(color % "UI/image/login3.png")
        
        self.button_close = QPushButton(' ', self)
        self.button_close.setGeometry(368, 0, 32, 25)
        self.button_close.setToolTip('关闭')
        self.button_close.setStyleSheet(color % "UI/image/login2.png")
        

        self.centralwidget1 = QWidget(self)
        self.centralwidget1.setGeometry(317, 50, 100, 40)
        self.gridLayout1 = QGridLayout(self.centralwidget1)
        self.centralwidget2 = QWidget(self)
        self.centralwidget2.setGeometry(317, 83, 100, 40)
        self.gridLayout2 = QGridLayout(self.centralwidget2)
        self.centralwidget3 = QWidget(self)
        self.centralwidget3.setGeometry(317, 116, 100, 40)
        self.gridLayout3 = QGridLayout(self.centralwidget3)

        # 定义获取焦点事件
        self.Edit_name.installEventFilter(self)
        self.Edit_password.installEventFilter(self)
        self.Edit_password2.installEventFilter(self)

        self.button_little.clicked.connect(self.showMinimized)
        self.button_alter.clicked.connect(self.onalter)
    
    # 定义获取焦点事件
    def eventFilter(self, obj, event):
        if obj == self.Edit_name:
            if event.type()== QEvent.FocusIn:
                self.name_Error_hint()
            return False
        elif obj == self.Edit_password:
            if event.type()== QEvent.FocusIn:
                self.password_Error_hint()
            return False
        elif obj == self.Edit_password2:
            if event.type()== QEvent.FocusIn:
                self.password_Error_hint2()
            return False

    def onalter(self):
        ypassword = self.Edit_name.text()
        password = self.Edit_password.text()
        password2 = self.Edit_password2.text()
        if 0 < len(ypassword) < 6:
            self.name_Error_hint('*密码最少6位')
            return
        elif  0 < len(password) < 6:
            self.password_Error_hint('*密码最少6位')
            return
        elif password != password2:
            self.password_Error_hint2('*密码不一致')
            return
        ypassword = hashlib.md5(self.Edit_name.text().\
                    encode(encoding='UTF-8')).hexdigest()
        password = hashlib.md5(self.Edit_password.text().\
                    encode(encoding='UTF-8')).hexdigest()
        data = 'N ' + self.user + ' ' + ypassword + ' ' + password
        self.timekey = True
        self.threadmes = MyThread(self.connfd,data)
        self.threadmes.messageSignal.connect(self.handle_return_message)
        self.threadmes.start()
    
    # 处理密码返回的情况处理
    def handle_return_message(self,mess):
        self.threadmes.deleteLater()
        if mess == 'NNO Bedefeated':
            self.password_Error_hint('*修改失败')
        elif mess == 'NOK ':
            self.password_Error_hint('*修改成功')
        elif mess == 'NNO PasswordRepetition':
            self.name_Error_hint('*输入错误')
        else:
            pass
        # 把按键检测变为False
        self.timekey = False

    def name_Error_hint(self,show=' '):
        try:
            sip.delete(self.user_hint)
        except AttributeError:
            pass
        pe_red = QPalette()
        pe_red.setColor(QPalette.WindowText,Qt.red)
        self.user_hint = QLabel(show,self.centralwidget1)
        self.user_hint.setPalette(pe_red)
        self.gridLayout1.addWidget(self.user_hint, 0, 0, 1, 1)
        QApplication.processEvents()
        
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
            self.close()
            self.close_signal.emit()
    
    #  把隐藏的窗口显示出来
    def handle_click(self,):
        if not self.isVisible():
            self.Edit_user.clear()
            self.Edit_name.clear()
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
        except:
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
