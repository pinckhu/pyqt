#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : $mymessage.py
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
from UI.mythread import MyThread
import time
import image
import sys
import sip


class MyMessage(QDialog):

    close_signal = pyqtSignal()
    altermess = pyqtSignal(str)

    def __init__(self, user,connfd):
        super(MyMessage,self).__init__()
        self.connfd = connfd
        self.user = user
        self.timekey = False
        self.page = 1
        self.haveornot = 1
        self.initUI()
    
    def initUI(self):
        # 创建固定窗口大小
        self.setFixedSize(445, 380)
        # 无边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(':/logo.png'))

        window_pale = QPalette()
        window_pale.setBrush(self.backgroundRole(),\
                    QBrush(QPixmap("UI/image/mymess.jpg"))) 
        self.setPalette(window_pale)

        # 程序名
        pee = QPalette()
        pee.setColor(QPalette.WindowText,Qt.white)
        self.lbl_main = QLabel('我发布的信息', self)
        self.lbl_main.move(10, 10)
        self.lbl_main.setPalette(pee)

        # 设置的一个无用的输入框 让启动时焦点不在输入框内
        self.lbl1_1 = QLineEdit(self)
        self.lbl1_1.setGeometry(-1, -1, 1, 1)
        self.button1_1 = QPushButton(self)
        self.button1_1.setGeometry(-1, -1, 1, 1)

        self.centralwidget = QWidget(self)
        self.centralwidget.setGeometry(20, 38, 400, 300)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.handle_page()

        self.centralwidget2 = QWidget(self)
        self.centralwidget2.setGeometry(30, 335, 100, 35)
        self.gridLayout2 = QGridLayout(self.centralwidget2)

        color3 = "QPushButton{border:none;color:rgb(0, 0, 0);}"\
                "QPushButton:hover{border-image: url(%s);border\
                :none;color:rgb(255, 255, 255);}"
        
        self.button_little = QPushButton(' ', self)                      # 创建最小化按钮
        self.button_little.setGeometry(381, 0, 32, 25)
        self.button_little.setToolTip('最小化')
        self.button_little.setStyleSheet(color3 % 'UI/image/login3.png')
        
        self.button_close = QPushButton(' ', self)                       # 创建关闭按钮
        self.button_close.setGeometry(413, 0, 32, 25)
        self.button_close.setToolTip('关闭')
        self.button_close.setStyleSheet(color3 % 'UI/image/login2.png')

        # 首页按钮
        self.button_homepage = QPushButton('首页', self)
        self.button_homepage.setGeometry(140, 335, 50, 35)
        self.button_homepage.setFlat(True)
        self.button_homepage.setStyleSheet(color3 % 'UI/image/focus.png')
        
        # 上一页按钮
        self.button_previouspage = QPushButton('上一页', self)
        self.button_previouspage.setGeometry(200, 335, 50, 35)
        self.button_previouspage.setFlat(True)
        self.button_previouspage.setStyleSheet(color3 % 'UI/image/focus.png')
        
        # 下一页按钮
        self.button_nextpage = QPushButton('下一页', self)
        self.button_nextpage.setGeometry(260, 335, 50, 35)
        self.button_nextpage.setFlat(True)
        self.button_nextpage.setStyleSheet(color3 % 'UI/image/focus.png')

        self.button_little.clicked.connect(self.showMinimized)
        self.button_homepage.clicked.connect(self.handle_button_homepage)
        self.button_previouspage.clicked.connect(self.handle_button_previouspage)
        self.button_nextpage.clicked.connect(self.handle_button_nextpage)
    
    # 第几页显示
    def handle_page_show(self):
        try:
            sip.delete(self.page_hint)
        except AttributeError:
            pass
        pee = QPalette()
        pee.setColor(QPalette.WindowText,Qt.white)
        self.page_hint = QLabel('第  %d  页' % self.page,self.centralwidget2)
        self.page_hint.setPalette(pee)
        self.gridLayout2.addWidget(self.page_hint, 0, 0, 1, 1)
        QApplication.processEvents()
    
    # 处理首页按钮
    def handle_button_homepage(self):
        if self.page == 1:
            return
        elif self.haveornot == 2 and self.page == 1:
            return
        elif self.timekey:
            return
        self.timekey = True
        self.page = 1
        self.handle_page()
    
    # 处理上一页按钮
    def handle_button_previouspage(self):
        if self.page == 1:
            return
        elif self.haveornot == 2 and self.page == 1:
            return
        elif self.timekey:
            return
        self.timekey = True
        self.page -= 1
        self.handle_page()
    
    # 处理下一页按钮
    def handle_button_nextpage(self):
        try:
            if self.haveornot == 2:
                return
            elif self.TheDataIsLessThan < 10:
                return
            elif self.timekey:
                return
        except:
            pass
        self.timekey = True
        self.page += 1
        self.handle_page()
    
    # 获取目录
    def handle_page(self):
        data = 'C ' + self.user + ' ' + str(self.page)
        self.threadmess = MyThread(self.connfd,data)
        self.threadmess.messageSignal.connect(self.handle_return_message)
        self.threadmess.start()
    
    # 处理返回回来的数据
    def handle_return_message(self,mess):
        self.threadmess.deleteLater()
        self.handle_page_show()
        if self.haveornot == 1:
            try:
                for i in range(10):
                    FindLE = self.findChild(QPushButton,str(self.catalogue[i]))
                    sip.delete(FindLE)
            except:
                    pass
        elif self.haveornot == 2:
            try:
                FindLE = self.findChild(QPushButton,'0')
                sip.delete(FindLE)
            except:
                    pass
        self.catalogue = [0,0,0,0,0,0,0,0,0,0]
        if mess == 'CFNO NoData':
            self.Button_no_mymess()
            self.timekey = False
            return
        mess = mess[3:].split(' ')
        self.TheDataIsLessThan = len(mess)
        self.message = []
        for i in range(10):
            try:
                self.message.extend([mess[i].split('#')])
                self.catalogue[i] = int(self.message[i][0])
            except:
                self.catalogue[i] = i-10
        self.Button_mymess()
        self.timekey = False
    
    def Button_no_mymess(self):
        self.haveornot = 2
        color = "QPushButton{border:none;color:rgb(118, 118, 118);}"\
                "QPushButton:hover{border:none;color:rgb(255, 168, 0);}"
        self.Button = QPushButton('没有数据', self)
        self.Button.setObjectName('0')
        self.Button.setStyleSheet(color)
        self.gridLayout.addWidget(self.Button, 0, 0, 1, 1)
        QApplication.processEvents()

    def fun(self):
        btn = self.sender()
        # 如果小于0就不执行
        index = btn.objectName()
        if int(index) < 0:
            return
        self.timekey = True
        data = 'U ' + index
        self.threadme = MyThread(self.connfd,data)
        self.threadme.messageSignal.connect(self.handle_return_alter_mess)
        self.threadme.start()

    def handle_return_alter_mess(self,mess):
        self.threadme.deleteLater()
        self.timekey = False
        if mess == 'UFNO NoData':
            return
        self.altermess.emit(mess[3:])

    def Button_mymess(self):
        self.haveornot = 1
        color = "QPushButton{border:none;color:rgb(118, 118, 118);}"\
                "QPushButton:hover{border:none;color:rgb(255, 168, 0);}"
        for i in range(10):
            try:
                timedisplay = round(time.time()) - int(self.message[i][5])
                if 0 <= timedisplay < 60 :
                    timedisplay = str(timedisplay) + '秒前发布'
                elif 0 < timedisplay // 60 < 60 :
                    timedisplay = str(timedisplay // 60) + '分钟前发布'
                elif 1 <= timedisplay // 3600 < 24 :
                    timedisplay = str(timedisplay // 3600) + '小时前发布'
                else:
                    timedisplay = str(timedisplay // 86400) + '天前发布'
                self.Button = QPushButton('%s/%s-%s/%s    %s' % \
                    (self.message[i][1],self.message[i][2],self.message[i][3],\
                    self.message[i][4],timedisplay), self, clicked=self.fun)
            except:
                self.Button = QPushButton(' ', self, clicked=self.fun)
            self.Button.setObjectName('%s' % self.catalogue[i])
            self.Button.setStyleSheet(color)
            self.gridLayout.addWidget(self.Button, i, 0, 1, 1)
            QApplication.processEvents()
    
    # 把隐藏的窗口显示出来
    def handle_click(self):
        if not self.isVisible():
            self.show()
    
    # 对ESC进行的重载  按ESC也有退出的功能
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
            self.close_signal.emit()
    
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