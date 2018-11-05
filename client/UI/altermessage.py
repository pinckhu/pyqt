#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : $altermessage.py
# @Author : Hu
# @Date   : 2018.10
# @Contact：pinckhu@sina.com
'''
该程序是编辑信息的窗口
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
                            QSpacerItem,QSizePolicy,\
                            QButtonGroup,QRadioButton,QTextEdit
from UI.mythread import MyThread
import image
import chardet
import time
import json
import sys
import sip

class AlterMessage(QDialog):

    close_signal = pyqtSignal()

    def __init__(self, mess,connfd):
        super(AlterMessage,self).__init__()
        self.connfd = connfd
        self.mess = mess.split('#')
        self.timekey = False
        self.data = ''
        self.initUI()
    
    def initUI(self):
        # 创建固定窗口大小
        self.setFixedSize(535, 600)
        # 窗口标题
        self.setWindowTitle('注册')
        # 无边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(':/logo.png'))

        window_pale = QPalette()
        window_pale.setBrush(self.backgroundRole(),\
                QBrush(QPixmap("UI/image/altermessage.jpg"))) 
        self.setPalette(window_pale)


        #设置字体颜色
        pe = QPalette()
        pe.setColor(QPalette.WindowText,Qt.white)
        # 程序名
        self.lbl_main = QLabel('修改货运信息', self)
        self.lbl_main.move(10, 10)
        self.lbl_main.setPalette(pe)


        # 创建发货地级联布局
        self.centralwidget = QWidget(self)
        self.centralwidget.setGeometry(90, 50, 400, 40)
        layout = QHBoxLayout(self.centralwidget)
        self.province_box = QComboBox(self, minimumWidth=30)  # 市级以上
        self.province_box.setMaxVisibleItems(35)
        self.city_box = QComboBox(self, minimumWidth=73)  # 市
        self.city_box.setMaxVisibleItems(35)
        self.county_box = QComboBox(self, minimumWidth=73)  # 市级以下
        self.county_box.setMaxVisibleItems(35)
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
        layout.addWidget(self.county_box)
        county = QLabel("区/县", self)
        county.setPalette(pe)
        layout.addWidget(county)
        
        # 创建目的地级联布局
        self.centralwidget2 = QWidget(self)
        self.centralwidget2.setGeometry(90, 96, 400, 40)
        layout2 = QHBoxLayout(self.centralwidget2)
        self.province_box2 = QComboBox(self, minimumWidth=30)  # 市级以上
        self.province_box2.setMaxVisibleItems(35)
        self.city_box2 = QComboBox(self, minimumWidth=73)  # 市
        self.city_box2.setMaxVisibleItems(35)
        self.county_box2 = QComboBox(self, minimumWidth=73)  # 市级以下
        self.county_box2.setMaxVisibleItems(35)
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
        layout2.addWidget(self.county_box2)
        county2 = QLabel("区/县", self)
        county2.setPalette(pe)
        layout2.addWidget(county2)
        self.initModel()
        self.initSignal()
        self.initData()

        for i in range(self.province_box.count()):
            if self.province_box.itemText(i) == self.mess[1]:
                self.province_box.setCurrentIndex(i)
                break
        for i in range(self.city_box.count()):
            if self.city_box.itemText(i) == self.mess[2]:
                self.city_box.setCurrentIndex(i)
                break
        for i in range(self.county_box.count()):
            if self.county_box.itemText(i) == self.mess[3]:
                self.county_box.setCurrentIndex(i)
                break
        for i in range(self.province_box2.count()):
            if self.province_box2.itemText(i) == self.mess[4]:
                self.province_box2.setCurrentIndex(i)
                break
        for i in range(self.city_box2.count()):
            if self.city_box2.itemText(i) == self.mess[5]:
                self.city_box2.setCurrentIndex(i)
                break
        for i in range(self.county_box2.count()):
            if self.county_box2.itemText(i) == self.mess[6]:
                self.county_box2.setCurrentIndex(i)
                break

        #设置字体颜色
        pe = QPalette()
        pe.setColor(QPalette.WindowText,Qt.darkGray)

        self.l = ['轻卡货车','中型货车','大型货车','自卸货车','半挂货车']
        x = 100
        self.bg1 = QButtonGroup(self)
        for i in range(len(self.l)):
            self.bu = QRadioButton(self.l[i],self)
            self.bu.setGeometry(x, 150, 75, 28)
            self.bu.setPalette(pe)
            self.bg1.addButton(self.bu, i)
            x += 80
        
        self.info1 = self.mess[7]
        self.bg1.buttonClicked.connect(self.rbclicked)
        self.bg1.buttons()[self.l.index(self.mess[7])].toggle()

        self.l2 = ['均货','重货','轻货','整车','零担']
        x = 100
        self.bg12 = QButtonGroup(self)
        for i in range(10,10+len(self.l2)):
            self.bu = QRadioButton(self.l2[i-10],self)
            self.bu.setGeometry(x, 180, 75, 28)
            # self.bu.toggle()
            self.bu.setPalette(pe)
            self.bg12.addButton(self.bu, i)
            x += 80

        self.info12 = self.mess[8]
        self.bg12.buttonClicked.connect(self.rbclicked)
        self.bg12.buttons()[self.l2.index(self.mess[8])].toggle() 

        self.l3 = ['普货','鲜货','冻货','大件设备']
        x = 100
        self.bg13 = QButtonGroup(self)
        for i in range(20,20+len(self.l3)):
            self.bu = QRadioButton(self.l3[i-20],self)
            self.bu.setGeometry(x, 210, 75, 28)
            self.bu.setPalette(pe)
            self.bg13.addButton(self.bu, i)
            x += 80
        
        self.info13 = self.mess[9]
        self.bg13.buttonClicked.connect(self.rbclicked)
        self.bg13.buttons()[self.l3.index(self.mess[9])].toggle() 

        self.l4 = ['无要求','20-50万','50-100万',\
                                    '100-300万','300万以上']
        x = 100
        self.bg14 = QButtonGroup(self)
        for i in range(30,30+len(self.l4)):
            self.bu = QRadioButton(self.l4[i-30],self)
            self.bu.setGeometry(x, 240, 75, 28)
            self.bu.setPalette(pe)
            self.bg14.addButton(self.bu, i)
            x += 80
        self.info14 = self.mess[10]
        self.bg14.buttonClicked.connect(self.rbclicked)
        self.bg14.buttons()[self.l4.index(self.mess[10])].toggle()

        conceal = "background:\
            transparent;border-width:0;border-style:outset"

        self.Edit_bulk = QLineEdit(self)
        self.Edit_bulk.setGeometry(100, 290, 100, 22)
        self.Edit_bulk.setPlaceholderText('方量')
        self.Edit_bulk.setStyleSheet(conceal)
        self.Edit_bulk.setValidator(QRegExpValidator\
                        (QRegExp(r"[0-9]+.?[0-9]?"),self))
        self.Edit_bulk.setMaxLength(6)
        self.Edit_bulk.setToolTip('方量最大长度6位')
        self.Edit_bulk.setText(self.mess[11])

        self.weight = QLineEdit(self)
        self.weight.setGeometry(245, 290, 100, 22)
        self.weight.setPlaceholderText('总吨位')
        self.weight.setStyleSheet(conceal)
        self.weight.setValidator(QRegExpValidator\
                    (QRegExp(r"[0-9]+.?[0-9]?"),self))
        self.weight.setMaxLength(6)
        self.weight.setToolTip('吨位最大长度6位')
        self.weight.setText(self.mess[12])

        self.Edit_total = QLineEdit(self)
        self.Edit_total.setGeometry(400, 290, 100, 22)
        self.Edit_total.setPlaceholderText('运费')
        self.Edit_total.setStyleSheet(conceal)
        self.Edit_total.setValidator(QRegExpValidator\
                                (QRegExp(r"[0-9]+"),self))
        self.Edit_total.setMaxLength(7)
        self.Edit_total.setToolTip('运费最大长度为6位的整数')
        self.Edit_total.setText(self.mess[13])

        self.text_describe = QTextEdit(self)
        self.text_describe.setGeometry(100, 340, 370, 150)
        self.text_describe.setToolTip('300字以内')
        self.text_describe.setStyleSheet(conceal)

        self.text_describe.setPlaceholderText('300字以内')
        self.text_describe.setPlainText(self.mess[15])

        self.Edit_phone = QLineEdit(self)
        self.Edit_phone.setGeometry(100, 518, 150, 22)
        self.Edit_phone.setPlaceholderText('手机号码')
        self.Edit_phone.setStyleSheet(conceal)
        self.Edit_phone.setValidator(QRegExpValidator\
                                (QRegExp(r"[0-9]+"),self))
        self.Edit_phone.setMaxLength(11)
        self.Edit_phone.setToolTip('联系电话11位')
        self.Edit_phone.setText(self.mess[14])

        l = ['请选择','12小时','24小时','3天内','5天内',\
                        '1周内','1月内','3月内','1年内','永久']
        self.combo = QComboBox(self)
        self.combo.addItems(l)
        self.combo.setGeometry(400, 518,70,20)
        validity = int(self.mess[17]) - int(self.mess[16])
        if validity == 43200:
            validity = '12小时'
        elif validity == 86400:
            validity = '24小时'
        elif validity == 259200:
            validity = '3天内'
        elif validity == 432000:
            validity = '5天内'
        elif validity == 604800:
            validity = '1周内'
        elif validity == 2592000:
            validity = '1月内'
        elif validity == 7776000:
            validity = '3月内'
        elif validity == 31536000:
            validity = '1年内'
        elif validity == 999999999:
            validity = '永久'
        for i in range(self.combo.count()):
            if self.combo.itemText(i) == validity:
                self.combo.setCurrentIndex(i)
                break

        color2 = "QPushButton{border:none;}"\
                "QPushButton:hover{border-image:url(%s);border:none;}"

        self.button_issue = QPushButton(' ', self)
        self.button_issue.setGeometry(100, 562, 230, 26)
        self.button_issue.setStyleSheet\
                            (color2 % 'UI/image/altermessage1.png')
        self.button_issue.clicked.connect(self.onissue)

        self.centralwidget = QWidget(self)
        self.centralwidget.setGeometry(350, 555, 150, 40)
        self.gridLayout = QGridLayout(self.centralwidget)
        # 定义获取焦点事件
        self.Edit_bulk.installEventFilter(self)
        self.Edit_total.installEventFilter(self)
        self.text_describe.installEventFilter(self)
        self.Edit_phone.installEventFilter(self)
        self.combo.installEventFilter(self)
        self.province_box.installEventFilter(self)
        self.city_box.installEventFilter(self)
        self.county_box.installEventFilter(self)
        self.province_box2.installEventFilter(self)
        self.city_box2.installEventFilter(self)
        self.county_box2.installEventFilter(self)

        self.button_little = QPushButton(' ', self)
        self.button_little.setGeometry(471, 0, 32, 25)
        self.button_little.setToolTip('最小化')
        self.button_little.setStyleSheet\
                            (color2 % 'UI/image/login3.png')
        
        self.button_close = QPushButton(' ', self)
        self.button_close.setGeometry(503, 0, 32, 25)
        self.button_close.setToolTip('关闭')
        self.button_close.setStyleSheet\
                            (color2 % 'UI/image/login2.png')

        self.button_little.clicked.connect(self.showMinimized)

    # 定义获取焦点事件
    def eventFilter(self, obj, event):
        if obj == self.Edit_bulk:
            if event.type()== QEvent.FocusIn:
                self.issue_Error_hint()
            return False
        elif obj == self.Edit_total:
            if event.type()== QEvent.FocusIn:
                self.issue_Error_hint()
            return False
        elif obj == self.text_describe:
            if event.type()== QEvent.FocusIn:
                self.issue_Error_hint()
            return False
        elif obj == self.Edit_phone:
            if event.type()== QEvent.FocusIn:
                self.issue_Error_hint()
            return False
        elif obj == self.combo:
            if event.type()== QEvent.FocusIn:
                self.issue_Error_hint()
            return False
        elif obj == self.province_box:
            if event.type()== QEvent.FocusIn:
                self.issue_Error_hint()
            return False
        elif obj == self.city_box:
            if event.type()== QEvent.FocusIn:
                self.issue_Error_hint()
            return False
        elif obj == self.county_box:
            if event.type()== QEvent.FocusIn:
                self.issue_Error_hint()
            return False
        elif obj == self.province_box2:
            if event.type()== QEvent.FocusIn:
                self.issue_Error_hint()
            return False
        elif obj == self.city_box2:
            if event.type()== QEvent.FocusIn:
                self.issue_Error_hint()
            return False
        elif obj == self.county_box2:
            if event.type()== QEvent.FocusIn:
                self.issue_Error_hint()
            return False
    
    def period_of_validity(self):
        now_time = round(time.time())
        if self.combo.currentText() == '12小时':
            endtime = str(now_time + 43200)
            return str(now_time) + '#' + endtime
        elif self.combo.currentText() == '24小时':
            endtime = str(now_time + 86400)
            return str(now_time) + '#' + endtime
        elif self.combo.currentText() == '3天内':
            endtime = str(now_time + 259200)
            return str(now_time) + '#' + endtime
        elif self.combo.currentText() == '5天内':
            endtime = str(now_time + 432000)
            return str(now_time) + '#' + endtime
        elif self.combo.currentText() == '1周内':
            endtime = str(now_time + 604800)
            return str(now_time) + '#' + endtime
        elif self.combo.currentText() == '1月内':
            endtime = str(now_time + 2592000)
            return str(now_time) + '#' + endtime
        elif self.combo.currentText() == '3月内':
            endtime = str(now_time + 7776000)
            return str(now_time) + '#' + endtime
        elif self.combo.currentText() == '1年内':
            endtime = str(now_time + 31536000)
            return str(now_time) + '#' + endtime
        elif self.combo.currentText() == '永久':
            endtime = str(now_time + 999999999)
            return str(now_time) + '#' + endtime

    def onissue(self):
        s_province = self.province_box.currentText()
        s_city = self.city_box.currentText()
        s_county = self.county_box.currentText()
        m_province = self.province_box2.currentText()
        m_city = self.city_box2.currentText()
        m_county = self.county_box2.currentText()

        if s_province == '请选择':
            self.issue_Error_hint('*没有选择起始位置')
            return
        elif m_province == '请选择':
            self.issue_Error_hint('*没有选择目的地')
            return
        elif not self.info1:
            self.issue_Error_hint('*没有选择要求车型')
            return
        elif not self.info12:
            self.issue_Error_hint('*没有选择货物类别')
            return
        elif not self.info13:
            self.issue_Error_hint('*没有选择货物性质')
            return
        elif not self.info14:
            self.issue_Error_hint('*没有选择要求保险')
            return
        elif not self.Edit_bulk.text():
            self.issue_Error_hint('*没有输入方量')
            return
        elif not self.weight.text():
            self.issue_Error_hint('*没有输入重量')
            return
        elif not self.Edit_total.text():
            self.issue_Error_hint('*没有输入总运费')
            return
        elif not self.text_describe.toPlainText():
            self.issue_Error_hint('*详细描述不能为空(没有请写无)')
            return
        elif self.combo.currentText() == '请选择':
            self.issue_Error_hint('*没有选择有效期')
            return
        for i in self.text_describe.toPlainText():
            if i in [' ','#']:
                self.issue_Error_hint('*详细描述中不能有【空格】')
                return
            elif i in [' ','#']:
                self.issue_Error_hint('*详细描述中不能有【#】')
                return 
        
        data = 'UX ' + self.mess[0] + ' ' + s_province + '#' + s_city + '#' +\
            s_county + '#' + m_province + '#' + m_city + '#' + m_county\
             + '#' + self.info1 + '#' + self.info12 + '#' + self.info13\
             + '#' + self.info14 + '#' + self.Edit_bulk.text()\
             + '#' + self.weight.text() + '#' + self.Edit_total.text()\
             + '#' + self.Edit_phone.text() + '#' + \
            self.text_describe.toPlainText()
        if self.data == data:
            return self.issue_Error_hint('*不能发布重复信息')
        self.data = data
        data = data + '#' + self.period_of_validity()
        # 让这个变量为True
        self.timekey = True
        self.threadmess = MyThread(self.connfd,data)
        self.threadmess.messageSignal.connect(self.handle_return_message)
        self.threadmess.start()
    
    # 处理返回的情况处理
    def handle_return_message(self,mess):
        self.threadmess.deleteLater()
        if mess == 'UXNO NoData':
            self.issue_Error_hint('*修改失败')
        elif mess == 'UXOK ':
            self.issue_Error_hint('*修改成功')
        else:
            pass
        # 把按键检测变为False
        self.timekey = False
    
    def issue_Error_hint(self,show=' '):
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

    
    def rbclicked(self):
        sender = self.sender()
        if sender == self.bg1:
            if self.bg1.checkedId() == 0:
                self.info1 = self.l[0]
            elif self.bg1.checkedId() == 1:
                self.info1 = self.l[1]
            elif self.bg1.checkedId() == 2:
                self.info1 = self.l[2]
            elif self.bg1.checkedId() == 3:
                self.info1 = self.l[3]
            elif self.bg1.checkedId() == 4:
                self.info1 = self.l[4]         
            else:
                self.info1 = ''
            self.issue_Error_hint()
        elif sender == self.bg12:
            if self.bg12.checkedId() == 10:
                self.info12 = self.l2[0]
            elif self.bg12.checkedId() == 11:
                self.info12 = self.l2[1]
            elif self.bg12.checkedId() == 12:
                self.info12 = self.l2[2]
            elif self.bg12.checkedId() == 13:
                self.info12 = self.l2[3]
            elif self.bg12.checkedId() == 14:
                self.info12 = self.l2[4]          
            else:
                self.info12 = ''
            self.issue_Error_hint()
        elif sender == self.bg13:
            if self.bg13.checkedId() == 20:
                self.info13 = self.l3[0]
            elif self.bg13.checkedId() == 21:
                self.info13 = self.l3[1]
            elif self.bg13.checkedId() == 22:
                self.info13 = self.l3[2]
            elif self.bg13.checkedId() == 23:
                self.info13 = self.l3[3]       
            else:
                self.info13 = ''
            self.issue_Error_hint()
        elif sender == self.bg14:
            if self.bg14.checkedId() == 30:
                self.info14 = self.l4[0]
            elif self.bg14.checkedId() == 31:
                self.info14 = self.l4[1]
            elif self.bg14.checkedId() == 32:
                self.info14 = self.l4[2]
            elif self.bg14.checkedId() == 33:
                self.info14 = self.l4[3]
            elif self.bg14.checkedId() == 34:
                self.info14 = self.l4[4]       
            else:
                self.info14 = ''
            self.issue_Error_hint()

    def initSignal(self):
        # 初始化信号槽
        self.province_box.currentIndexChanged.connect\
                                (self.city_model.setFilter)
        self.city_box.currentIndexChanged.connect\
                                (self.county_model.setFilter)
        self.province_box2.currentIndexChanged.connect\
                                (self.city_model2.setFilter)
        self.city_box2.currentIndexChanged.connect\
                                (self.county_model2.setFilter)

    def initModel(self):
        # 初始化模型
        self.province_model = SortFilterProxyModel(self)
        self.city_model = SortFilterProxyModel(self)
        self.county_model = SortFilterProxyModel(self)
        # 设置模型
        self.province_box.setModel(self.province_model)
        self.city_box.setModel(self.city_model)
        self.county_box.setModel(self.county_model)
        
        # 初始化模型
        self.province_model2 = SortFilterProxyModel(self)
        self.city_model2 = SortFilterProxyModel(self)
        self.county_model2 = SortFilterProxyModel(self)
        # 设置模型
        self.province_box2.setModel(self.province_model2)
        self.city_box2.setModel(self.city_model2)
        self.county_box2.setModel(self.county_model2)

    def initData(self):
        # 初始化数据
        datas = open("UI/data.json", "rb").read()
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
            else:  # 市以下
                self.county_model.appendRow(item)
        
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
            else:  # 市以下
                self.county_model2.appendRow(item)

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
            self.show()

    # 对ESC进行的重载  按ESC也有退出的功能
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
            self.close_signal.emit()
    
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