#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : $mainui.py
# @Author : Hu
# @Date   : 2018.10
# @Contact：pinckhu@sina.com
'''
该程序是主窗口
'''
from PyQt5.QtCore import Qt, pyqtSignal,QRegExp,QEvent,\
                        QPoint,QSortFilterProxyModel
from PyQt5.QtGui import QEnterEvent, QColor,QPixmap,QIcon,\
                        QPalette,QRegExpValidator,QCursor,\
                        QMouseEvent,QBrush,\
                        QStandardItemModel,QStandardItem,QFont
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel,\
                            QPushButton,QApplication,QLabel,\
                            QLineEdit,QWidget,QDesktopWidget,\
                            QMessageBox,QHBoxLayout,QComboBox,\
                            QSpacerItem,QSizePolicy,QTextEdit
from UI.mythread import MyThread
import image
import chardet
import time
import json
import sys
import sip


class MainWindow(QDialog):

    logoutSignal = pyqtSignal()

    def __init__(self, user,connfd):
        super(MainWindow, self).__init__()
        self.connfd = connfd
        self.user = user
        self.close_mess = '确认关闭'
        self.close_hint = '你是否确定退出'
        self.timekey = False
        self.page = 1
        self.haveornot = 1
        self.haveornot_records = 1
        self.initUi()

    def initUi(self):
        # 创建固定窗口大小
        self.setFixedSize(1024, 720)
        # 窗口标题
        self.setWindowTitle('货运信息公共平台')
        # 无边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(':/logo.png'))

        window_pale = QPalette()                           # 创建窗口背景图片对象
        window_pale.setBrush(self.backgroundRole(),\
                QBrush(QPixmap("UI/image/mainui.jpg")))        # 按指定路径找到图片
        self.setPalette(window_pale)

        #设置字体颜色
        pe = QPalette()
        pe.setColor(QPalette.WindowText,Qt.white)
        pee = QPalette()
        pee.setColor(QPalette.WindowText, Qt.white)

        # 程序名
        self.lbl_main = QLabel('货运信息公共平台', self)
        self.lbl_main.move(10, 10)
        self.lbl_main.setPalette(pee)

        self.color = "QPushButton{border-image: url(%s);border:none;}"\
                 "QPushButton:hover{border-image: url(%s);border:none;}"

        # 最小化按钮
        self.button_min = QPushButton(' ', self)
        self.button_min.setGeometry(940, 2, 43, 26)
        self.button_min.setFlat(True)
        self.button_min.setToolTip('最小化')
        self.button_min.setStyleSheet(self.color % \
                ('UI/image/mainmin1.png','UI/image/mainmin2.png'))

        # 关闭按钮
        self.button_close = QPushButton(' ', self)
        self.button_close.setGeometry(976, 2, 43, 26)
        self.button_close.setFlat(True)
        self.button_close.setToolTip('关闭')
        self.button_close.setStyleSheet(self.color % \
                ('UI/image/mainclose1.png','UI/image/mainclose2.png'))

        color2 = "QPushButton{border:none;color:rgb(55, 255, 255);}"\
                "QPushButton:hover{border-image: url(%s);border\
                :none;color:rgb(255, 255, 255);}"
        
        color3 = "QPushButton{border:none;color:rgb(255, 255, 255);}"\
                "QPushButton:hover{border-image: url(%s);border\
                :none;color:rgb(55, 255, 255);}"
        
        # 先判别一下昵称的长度
        button_user_lang = len(self.user) * 10 + 60

        # 显示登陆的账号 点击退出
        self.button_user = QPushButton('【%s】登陆中' % self.user, self)
        self.button_user.setGeometry(20, 40, button_user_lang, 35)
        self.button_user.setToolTip('点击退出此账号')
        self.button_user.setStyleSheet(color2 % '')
        
        # 发布信息按钮
        self.button_newmessage = QPushButton('发布信息', self)
        self.button_newmessage.setGeometry(670, 40, 60, 35)
        self.button_newmessage.setStyleSheet(color3 % 'UI/image/focus.png')
        
        # 我的发布按钮
        self.button_mymessage = QPushButton('我的发布', self)
        self.button_mymessage.setGeometry(750, 40, 60, 35)
        self.button_mymessage.setStyleSheet(color3 % 'UI/image/focus.png')

        color4 = "QPushButton{border:none;color:rgb(55, 255, 255);}"\
                "QPushButton:hover{border:none;color:rgb(55, 255, 255);}"

        # 历史记录按钮
        self.button_record = QPushButton('浏览记录', self)
        self.button_record.setGeometry(830, 40, 60, 35)
        self.button_record.setStyleSheet(color4)
        
        # 个人资料按钮
        self.button_data = QPushButton('个人资料', self)
        self.button_data.setGeometry(910, 40, 60, 35)
        self.button_data.setStyleSheet(color3 % 'UI/image/focus.png')
        
        # 创建发货地级联布局
        self.centralwidget = QWidget(self)
        self.centralwidget.setGeometry(70, 160, 240, 40)
        layout = QHBoxLayout(self.centralwidget)
        self.province_box = QComboBox(self, minimumWidth=30)  # 市级以上
        self.province_box.setMaxVisibleItems(35)
        self.city_box = QComboBox(self, minimumWidth=73)  # 市
        self.city_box.setMaxVisibleItems(35)
        layout.addWidget(self.province_box)
        province = QLabel("省", self)
        province.setPalette(pe)
        layout.addWidget(province)
        layout.addItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addWidget(self.city_box)
        city = QLabel("市", self)
        city.setPalette(pe)
        layout.addWidget(city)
        layout.addItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # 创建目的地级联布局
        self.centralwidget2 = QWidget(self)
        self.centralwidget2.setGeometry(307, 160, 240, 40)
        layout2 = QHBoxLayout(self.centralwidget2)
        self.province_box2 = QComboBox(self, minimumWidth=30)  # 市级以上
        self.province_box2.setMaxVisibleItems(35)
        self.city_box2 = QComboBox(self, minimumWidth=73)  # 市
        self.city_box2.setMaxVisibleItems(35)
        layout2.addWidget(self.province_box2)
        province2 = QLabel("省", self)
        province2.setPalette(pe)
        layout2.addWidget(province2)
        layout2.addItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout2.addWidget(self.city_box2)
        city2 = QLabel("市", self)
        city2.setPalette(pe)
        layout2.addWidget(city2)
        layout2.addItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.initModel()
        self.initSignal()
        self.initData()

        # 查找按钮
        self.button_find = QPushButton(' ', self)
        self.button_find.setGeometry(534, 93, 104, 129)
        self.button_find.setFlat(True)
        self.button_find.setStyleSheet(self.color % \
                                ('','UI/image/mainfind2.png'))

        color5 = "QPushButton{border:none;color:rgb(0, 0, 0);}"\
                "QPushButton:hover{border-image: url(%s);border\
                :none;color:rgb(255, 255, 255);}"
        
        # 首页按钮
        self.button_homepage = QPushButton('首页', self)
        self.button_homepage.setGeometry(250, 670, 50, 35)
        self.button_homepage.setFlat(True)
        self.button_homepage.setStyleSheet(color5 % 'UI/image/focus.png')
        
        # 上一页按钮
        self.button_previouspage = QPushButton('上一页', self)
        self.button_previouspage.setGeometry(310, 670, 50, 35)
        self.button_previouspage.setFlat(True)
        self.button_previouspage.setStyleSheet(color5 % 'UI/image/focus.png')
        
        # 下一页按钮
        self.button_nextpage = QPushButton('下一页', self)
        self.button_nextpage.setGeometry(370, 670, 50, 35)
        self.button_nextpage.setFlat(True)
        self.button_nextpage.setStyleSheet(color5 % 'UI/image/focus.png')

        self.versions = QLabel('版本号 v18.10', self)
        self.versions.move(900, 685)
        
        # 创建展示信息目录布局
        self.centralwidget = QWidget(self)
        self.centralwidget.setGeometry(77, 253, 550, 410)
        self.gridLayout = QGridLayout(self.centralwidget)

        # 第几页面显示
        self.centralwidget2 = QWidget(self)
        self.centralwidget2.setGeometry(60, 670, 100, 35)
        self.gridLayout2 = QGridLayout(self.centralwidget2)

        # 创建历史记录按钮布局
        self.centralwidget_record = QWidget(self)
        self.centralwidget_record.setGeometry(679, 95, 300, 130)
        self.gridLayout_record = QGridLayout(self.centralwidget_record)

        # # 创建详细信息布局
        self.cenparticulars = QWidget(self)
        self.cenparticulars.setGeometry(679, 260, 300, 350)
        self.cenparticulars_1 = QWidget(self)
        self.cenparticulars_1.setGeometry(685, 260, 250, 40)
        self.gridLayout_particulars_1 = QGridLayout(self.cenparticulars_1)
        self.cenparticulars_2 = QWidget(self)
        self.cenparticulars_2.setGeometry(685, 300, 100, 170)
        self.gridLayout_particulars_2 = QGridLayout(self.cenparticulars_2)
        self.cenparticulars_3 = QWidget(self)
        self.cenparticulars_3.setGeometry(755, 300, 100, 151)
        self.gridLayout_particulars_3 = QGridLayout(self.cenparticulars_3)
        self.cenparticulars_4 = QWidget(self)
        self.cenparticulars_4.setGeometry(753, 435, 215, 185)
        self.gridLayout_particulars_4 = QGridLayout(self.cenparticulars_4)
        self.cenparticulars_5 = QWidget(self)
        self.cenparticulars_5.setGeometry(685, 615, 250, 40)
        self.gridLayout_particulars_5 = QGridLayout(self.cenparticulars_5)


        # 定义按键信号和事件绑定
        self.button_min.clicked.connect(self.showMinimized)
        self.button_close.clicked.connect(self.close)
        
        self.button_user.clicked.connect(self.onuser)
        self.button_find.clicked.connect(self.onfind)
        self.button_homepage.clicked.connect(self.handle_button_homepage)
        self.button_previouspage.clicked.connect(self.handle_button_previouspage)
        self.button_nextpage.clicked.connect(self.handle_button_nextpage)

    # 处理详细信息事件显示
    def bel_particulars(self,mess):
        try:
            sip.delete(self.line_0)
            sip.delete(self.line_1_0)
            sip.delete(self.line_1_1)
            sip.delete(self.line_2_0)
            sip.delete(self.line_2_1)
            sip.delete(self.line_3_0)
            sip.delete(self.line_3_1)
            sip.delete(self.line_4_0)
            sip.delete(self.line_4_1)
            sip.delete(self.line_5_0)
            sip.delete(self.line_5_1)
            sip.delete(self.line_6_0)
            sip.delete(self.line_6_1)
            sip.delete(self.line_7_0)
            sip.delete(self.line_7_1)
            sip.delete(self.line_8_0)
            sip.delete(self.line_8_1)
            sip.delete(self.line_9_0)
        except:
            pass
        mess = mess.split('#')
        self.cenparticulars.setStyleSheet("background:#FFF;")
        styles = "color:#666;"
        styless = "color:#666;font-weight:bold;"
        self.line_0 = QLabel('%s/%s-%s/%s' % (mess[3],mess[4],mess[6],mess[7]),\
                         self.cenparticulars_1)
        self.line_0.setStyleSheet("font-size:16px;color:#1A303E;font-weight:bold;")
        self.gridLayout_particulars_1.addWidget(self.line_0, 0, 0)
        self.line_1_0 = QLabel('要求车型：', self.cenparticulars)
        self.gridLayout_particulars_2.addWidget(self.line_1_0, 0, 0)
        self.line_1_0.setStyleSheet(styless)
        self.line_1_1 = QLabel(mess[8], self.cenparticulars) 
        self.gridLayout_particulars_3.addWidget(self.line_1_1, 0, 0)
        self.line_1_1.setStyleSheet(styles)
        self.line_2_0 = QLabel('货物类别：', self.cenparticulars)
        self.gridLayout_particulars_2.addWidget(self.line_2_0, 1, 0)
        self.line_2_0.setStyleSheet(styless)
        self.line_2_1 = QLabel(mess[9], self.cenparticulars) 
        self.gridLayout_particulars_3.addWidget(self.line_2_1, 1, 0)
        self.line_2_1.setStyleSheet(styles)
        self.line_3_0 = QLabel('货物性质：', self.cenparticulars)
        self.gridLayout_particulars_2.addWidget(self.line_3_0, 2, 0)
        self.line_3_0.setStyleSheet(styless)
        self.line_3_1 = QLabel(mess[10], self.cenparticulars) 
        self.gridLayout_particulars_3.addWidget(self.line_3_1, 2, 0)
        self.line_3_1.setStyleSheet(styles)
        self.line_4_0 = QLabel('要求保险：', self.cenparticulars)
        self.gridLayout_particulars_2.addWidget(self.line_4_0, 3, 0)
        self.line_4_0.setStyleSheet(styless)
        self.line_4_1 = QLabel(mess[11], self.cenparticulars) 
        self.gridLayout_particulars_3.addWidget(self.line_4_1, 3, 0)
        self.line_4_1.setStyleSheet(styles)
        self.line_5_0 = QLabel('总方量：', self.cenparticulars)
        self.gridLayout_particulars_2.addWidget(self.line_5_0, 4, 0)
        self.line_5_0.setStyleSheet(styless)
        self.line_5_1 = QLabel(mess[12] + '方', self.cenparticulars) 
        self.gridLayout_particulars_3.addWidget(self.line_5_1, 4, 0)
        self.line_5_1.setStyleSheet(styles)
        self.line_6_0 = QLabel('总吨位：', self.cenparticulars)
        self.gridLayout_particulars_2.addWidget(self.line_6_0, 5, 0)
        self.line_6_0.setStyleSheet(styless)
        self.line_6_1 = QLabel(mess[13] + '顿', self.cenparticulars) 
        self.gridLayout_particulars_3.addWidget(self.line_6_1, 5, 0)
        self.line_6_1.setStyleSheet(styles)
        self.line_7_0 = QLabel('总运费：', self.cenparticulars)
        self.gridLayout_particulars_2.addWidget(self.line_7_0, 6, 0)
        self.line_7_0.setStyleSheet(styless)
        self.line_7_1 = QLabel(mess[14] + '元', self.cenparticulars) 
        self.gridLayout_particulars_3.addWidget(self.line_7_1, 6, 0)
        self.line_7_1.setStyleSheet(styles)
        self.line_8_0 = QLabel('详细描述：', self.cenparticulars)
        self.gridLayout_particulars_2.addWidget(self.line_8_0, 7, 0)
        self.line_8_0.setStyleSheet(styless)
        self.line_8_1 = QTextEdit(mess[16], self.cenparticulars) 
        self.gridLayout_particulars_4.addWidget(self.line_8_1, 0, 0)
        self.line_8_1.setReadOnly(True)
        self.line_8_1.setStyleSheet("border:0;color:#666;")
        self.line_9_0 = QLabel('联系电话：%s-%s-%s' % \
            (mess[15][:3],mess[15][3:7],mess[15][7:]), self.cenparticulars)
        self.line_9_0.setStyleSheet("font-size:16px;color:red;font-weight:bold;")
        self.gridLayout_particulars_5.addWidget(self.line_9_0, 0, 0)
        QApplication.processEvents()
    
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
    
    # 获取目录
    def handle_page(self):
        s_city = self.city_box.currentText()
        m_city = self.city_box2.currentText()
        data = 'H ' + s_city  + ' ' + m_city + ' ' + str(self.page)
        self.threadmess = MyThread(self.connfd,data)
        self.threadmess.messageSignal.connect(self.handle_return_message)
        self.threadmess.start()
    
    # 获取浏览记录目录
    def handle_records(self):
        data = 'M ' + self.user
        self.thread_records = MyThread(self.connfd,data)
        self.thread_records.messageSignal.connect(self.handle_return_records)
        self.thread_records.start()
    
    # 处理浏览记录目录返回回来的数据
    def handle_return_records(self,mess):
        self.thread_records.deleteLater()
        if self.haveornot_records == 1:
            try:
                for i in range(6):
                    FindLE = self.findChild(QPushButton,str(self.catalogue_records[i]))
                    sip.delete(FindLE)
            except:
                pass
        elif self.haveornot_records == 2:
            try:
                FindLE = self.findChild(QPushButton,'00')
                sip.delete(FindLE)
            except:
                pass
        self.catalogue_records = [0,0,0,0,0,0]
        if mess == 'MFNO NoData':
            self.Button_no_records()
            return
        mess = mess[3:].split(' ')
        self.message_records = []
        for i in range(6):
            try:
                self.message_records.extend([mess[i].split('#')])
                self.catalogue_records[i] = int(self.message_records[i][0])-100
            except:
                self.catalogue_records[i] = i-10
        self.Button_records()
    
    # 无浏览记录
    def Button_no_records(self):
        self.haveornot_records = 2
        color = "QPushButton{border:none;color:rgb(118, 118, 118);}"\
                "QPushButton:hover{border:none;color:rgb(255, 168, 0);}"
        self.Button = QPushButton('没有浏览记录', self)
        self.Button.setObjectName('00')
        self.Button.setStyleSheet(color)
        self.gridLayout_record.addWidget(self.Button, 0, 0, 1, 1)
        QApplication.processEvents()
    
    # 有浏览记录时
    def Button_records(self):
        self.haveornot_records = 1
        color = "QPushButton{border:none;color:rgb(118, 118, 118);}"\
                "QPushButton:hover{border:none;color:rgb(255, 168, 0);}"
        for i in range(6):
            try:
                timedisplay = round(time.time()) - int(self.message_records[i][5])
                if timedisplay < 60 :
                    if timedisplay < 1:
                        timedisplay = 1
                    timedisplay = str(timedisplay) + '秒前浏览'
                elif 0 < timedisplay // 60 < 60 :
                    timedisplay = str(timedisplay // 60) + '分钟前浏览'
                elif 1 <= timedisplay // 3600 < 24 :
                    timedisplay = str(timedisplay // 3600) + '小时前浏览'
                else:
                    timedisplay = str(timedisplay // 86400) + '天前浏览'
                self.Button = QPushButton\
                    ('%s/%s-%s/%s     %s' % (self.message_records[i][1],\
                    self.message_records[i][2],self.message_records[i][3],\
                    self.message_records[i][4],timedisplay), self, clicked=self.fun)
            except:
                self.Button = QPushButton(' ', self, clicked=self.fun)
            self.Button.setObjectName('%s' % self.catalogue_records[i])
            self.Button.setStyleSheet(color)
            self.gridLayout_record.addWidget(self.Button, i, 0, 1, 1)
            QApplication.processEvents()

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
        if mess == 'HFNO NoData':
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

    # 处理请求详细信息
    def fun(self):
        btn = self.sender()
        # 如果小于0就不执行
        # 如果小于100 取绝对值
        index = int(btn.objectName())
        if -11 < index < 0:
            return
        elif index < -50:
            index = abs(index + 100)
        self.timekey = True
        data = 'X ' + self.user + ' ' + str(index)
        self.thread_detail = MyThread(self.connfd,data)
        self.thread_detail.messageSignal.connect(self.handle_return_detail)
        self.thread_detail.start()
    
    # 处理请求详细信息返回来的数据
    def handle_return_detail(self,mess):
        self.thread_detail.deleteLater()
        self.bel_particulars(mess[3:])
        self.handle_records()
        self.timekey = False

    def Button_mymess(self):
        self.haveornot = 1
        color = "QPushButton{border:none;color:rgb(118, 118, 118);}"\
                "QPushButton:hover{border-image:url(UI/image/catalogue.png);\
                border:none;color:rgb(255, 255, 255);}"
        color2 = "QPushButton{border:none;color:rgb(118, 118, 118);}"\
                "QPushButton:hover{border:none;color:rgb(255, 255, 255);}"
        for i in range(10):
            try:
                timedisplay = round(time.time()) - int(self.message[i][12])
                if 0 <= timedisplay < 60 :
                    timedisplay = str(timedisplay) + '秒前发布'
                elif 0 < timedisplay // 60 < 60 :
                    timedisplay = str(timedisplay // 60) + '分钟前发布'
                elif 1 <= timedisplay // 3600 < 24 :
                    timedisplay = str(timedisplay // 3600) + '小时前发布'
                else:
                    timedisplay = str(timedisplay // 86400) + '天前发布'
                self.Button = QPushButton\
                    ('[%d]%s/%s-%s/%s       %s\n%s/%s/%s/%s/%s方/%s吨/%s元' % \
                    (i+1,self.message[i][1],self.message[i][2],self.message[i][3],\
                    self.message[i][4],timedisplay,self.message[i][5],\
                    self.message[i][6],self.message[i][7],self.message[i][8],\
                    self.message[i][9],self.message[i][10],self.message[i][11]),\
                     self, clicked=self.fun)
                self.Button.setStyleSheet(color)
            except:
                self.Button = QPushButton(' \n\n \n \n \n\n', self, clicked=self.fun)
                self.Button.setStyleSheet(color2)
            self.Button.setObjectName('%s' % self.catalogue[i])
            self.gridLayout.addWidget(self.Button, i, 0, 1, 1)
        QApplication.processEvents()
    
    #查找按钮事件处理
    def onfind(self):
        if self.timekey:
            return
        self.page = 1
        self.timekey = True
        self.handle_page()
    
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
    
    #  把隐藏的窗口显示出来
    def handle_click(self,):
        if not self.isVisible():
            self.show()
            time.sleep(0.1)
            self.onfind()
            time.sleep(0.1)
            self.handle_records()
    
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
    
    #级联联动处理
    def initSignal(self):
        # 初始化信号槽
        self.province_box.currentIndexChanged.connect(self.city_model.setFilter)
        self.province_box2.currentIndexChanged.connect(self.city_model2.setFilter)

    def initModel(self):
        # 初始化模型
        self.province_model = SortFilterProxyModel(self)
        self.city_model = SortFilterProxyModel(self)
        # 设置模型
        self.province_box.setModel(self.province_model)
        self.city_box.setModel(self.city_model)
        
        # 初始化模型
        self.province_model2 = SortFilterProxyModel(self)
        self.city_model2 = SortFilterProxyModel(self)
        # 设置模型
        self.province_box2.setModel(self.province_model2)
        self.city_box2.setModel(self.city_model2)

    def initData(self):
        # 初始化数据
        try:
            datas = open("UI/data.json", "rb").read()
        except:
            pass
        encoding = chardet.detect(datas) or {}
        datas = datas.decode(encoding.get("encoding", "utf-8"))
        datas = json.loads(datas)
        # 开始解析数据
        for data in datas:
            item_code = data.get("item_code")  # 编码
            item_name = data.get("item_name")  # 名字
            item = QStandardItem(item_name)
            item.setData(item_code, Qt.ToolTipRole)
            if item_code.endswith("0000"):  # 4个0结尾的是市级以上的
                self.province_model.appendRow(item)
            elif item_code.endswith("00"):  # 2个0结尾的是市
                self.city_model.appendRow(item)
        
        # 开始解析数据
        for data in datas:
            item_code = data.get("item_code")  # 编码
            item_name = data.get("item_name")  # 名字
            item = QStandardItem(item_name)
            item.setData(item_code, Qt.ToolTipRole)
            if item_code.endswith("0000"):  # 4个0结尾的是市级以上的
                self.province_model2.appendRow(item)
            elif item_code.endswith("00"):  # 2个0结尾的是市
                self.city_model2.appendRow(item)
    
    def onuser(self):
        self.close_mess = '确认注销'
        self.close_hint = '你是否确定注销'

    #窗口关闭提示
    def closeEvent(self, event):
        reply = QMessageBox.question(self, self.close_mess, self.close_hint,
                                     QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            if self.close_mess == '确认注销':
                self.logoutSignal.emit()
            elif self.close_mess == '确认关闭':
                try:
                    self.connfd.close()
                except AttributeError:
                    pass
            event.accept()
        else:
            event.ignore()
            self.close_mess = '确认关闭'
            self.close_hint = '你是否确定退出'

    # 对ESC进行的重载  按ESC也有退出的功能
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
    
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


class SortFilterProxyModel(QSortFilterProxyModel):

    def __init__(self, *args, **kwargs):
        super(SortFilterProxyModel, self).__init__(*args, **kwargs)
        self.setFilterRole(Qt.ToolTipRole)  # 根据Qt.ToolTipRole角色过滤
        self._model = QStandardItemModel(self)
        self.setSourceModel(self._model)

    def appendRow(self, item):
        self._model.appendRow(item)

    def setFilter(self, _):
        # 过滤
        # self.sender()#发送者
        # 获取上一个下拉框中的item_code
        item_code = self.sender().currentData(Qt.ToolTipRole)
        if not item_code:
            return
        if item_code.endswith("0000"):  # 过滤市
            self.setFilterRegExp(QRegExp(item_code[:-4] + "\d\d00"))
        elif item_code.endswith("00"):  # 过滤市以下
            self.setFilterRegExp(QRegExp(item_code[:-2] + "\d\d"))