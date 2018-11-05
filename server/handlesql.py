#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : $carserver.py
# @Author : Fire organize
# @Date   : 2018.10
# @Contact：xxxx

import pymysql
import time


class HandleSql(object):
    '''
    这是一个对数据交互的类
    '''
    def __init__(self,host='localhost',user='root',\
                        password='123456',database='car'):
        # 初始化
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        # 创建一个对数据库操作的对象
        self.db = pymysql.connect(self.host,self.user,\
                            self.password,self.database)
        # 绑定一个游标
        self.cursor = self.db.cursor()
        print('连接到数据库成功')
    
    # 验证用户是否在caruser表中是否存在
    def handle_user(self,user):
        sql = 'select password from caruser where userphone="%s";'
        self.cursor.execute(sql % user)
        ress = self.cursor.fetchone()
        return ress

    # 把注册信息插入到caruser表中
    def handle_register(self,user,password):
        sql = 'insert into caruser (userphone,password,registertime)\
                                         values ("%s","%s","%s");'
        now_time = round(time.time())
        try:                                 
            self.cursor.execute(sql % (user,password,str(now_time)))
            self.db.commit()
        except:
            self.db.rollback()
            return 'NO'
    
    # 更改caruser表中的用户密码
    def handle_password(self,user,password):
        sql = 'update caruser set password="%s" where userphone="%s";'
        try:                                 
            self.cursor.execute(sql % (password,user))
            self.db.commit()
        except:
            self.db.rollback()
            return 'NO'
    
    # 从message表中查询货运信息目录
    def handle_catalogue(self,origin,goal,page):
        now_time = round(time.time())
        if origin == '请选择' and goal == '请选择':
            sql = 'select id,origin_city,origin_county,\
            destination_city,destination_county,car_type,\
            cargo_type,cargo_property,insurance,cargo_volume,\
            cargo_weight,cargo_total_prices,release_time \
            from message where %d < end_time order by release_time DESC \
            limit %d,10;' % (now_time,(int(page)-1)*10)
        elif origin == '请选择' and goal != '请选择':
            sql = 'select id,origin_city,origin_county,\
            destination_city,destination_county,car_type,\
            cargo_type,cargo_property,insurance,cargo_volume,\
            cargo_weight,cargo_total_prices,release_time \
            from message where destination_city="%s"\
             and %d < end_time order by release_time DESC \
            limit %d,10;' % (goal,now_time,(int(page)-1)*10)
        elif origin != '请选择' and goal == '请选择':
            sql = 'select id,origin_city,origin_county,\
            destination_city,destination_county,car_type,\
            cargo_type,cargo_property,insurance,cargo_volume,\
            cargo_weight,cargo_total_prices,release_time \
            from message where origin_city="%s"\
             and %d < end_time order by release_time DESC \
            limit %d,10;' % (origin,now_time,(int(page)-1)*10)
        elif origin != '请选择' and goal != '请选择':
            sql = 'select id,origin_city,origin_county,\
                destination_city,destination_county,car_type,\
                cargo_type,cargo_property,insurance,cargo_volume,\
                cargo_weight,cargo_total_prices,release_time \
                from message where origin_city="%s" and destination_city="%s"\
                and %d < end_time order by release_time DESC \
                limit %d,10;' % (origin,goal,now_time,(int(page)-1)*10)
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    # 从cookies表中读取到用户的浏览记录的id 然后对message表查找每条记录信息
    def handle_history(self,user):
        sql = 'select message_id,browse_time from cookies \
                    where userphone="%s" order by browse_time DESC limit 0,6;'
        self.cursor.execute(sql % user)
        cookies = self.cursor.fetchall()
        if cookies == ():
            return 'NO'
        res = 'MF'
        for i in range(len(cookies)):
            sql = 'select id,origin_city,origin_county,destination_city,\
                        destination_county from message where id="%s";'
            self.cursor.execute(sql % cookies[i][0])
            try:
                l = [str(a) for a in self.cursor.fetchone()]
                l.append(str(cookies[i][1]))
                res += ' '
                res += '#'.join(l)
            except:
                pass
        return res
    
    # 用户浏览id编号的详细信息
    def handle_detail(self,user,id):
        sql = 'select * from message where id="%s";'
        self.cursor.execute(sql % id)
        res = self.cursor.fetchone()
        now_time = round(time.time())
        self.cursor.execute\
            ('select * from cookies where message_id="%s" and userphone="%s";' % (id,user))
        ress = self.cursor.fetchone()
        if ress == None:
            sql = 'insert into cookies value(NULL,"%s","%s","%s");'
            try:
                self.cursor.execute(sql % (user,id,str(now_time)))
                self.db.commit()
            except:
                self.db.rollback()
        else:
            sql = 'update cookies set browse_time="%s" where message_id="%s";'
            self.cursor.execute(sql % (str(now_time),id))
        return res
    
    # 把用户发布的一条详细信息插入到message表中
    def handle_publish(self,user,message):
        sql = 'insert into message value (NULL,"%s","%s","%s","%s","%s","%s",\
                "%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");'
        mess = (user + '#' + message).split('#')
        try:                                 
            self.cursor.execute(sql % tuple(mess))
            self.db.commit()
        except:
            self.db.rollback()
            return 'NO'
    
    # 查询message表中用户发布过信息
    def handle_mypublish(self,user,page):
        sql = 'select id,origin_city,origin_county,destination_city,\
                destination_county,release_time from message where\
                 userphone="%s" order by release_time DESC limit %d,10;'
        self.cursor.execute(sql % (user,(int(page)-1)*10))
        mypublish = self.cursor.fetchall()
        if mypublish == ():
            return 'NO'
        return mypublish

    # 用户编辑message中自己发布的一条信息
    def handle_compile(self,id):
        sql = 'select * from message where id="%s";'
        self.cursor.execute(sql % id)
        res = self.cursor.fetchone()
        if res == None:
            return 'NO'
        return res
    
    # 对编辑过的信息执行修改操作
    def handle_save_compile(self,id,message):
        sql = 'update message set origin_p="%s",origin_city="%s",\
                origin_county="%s",destination_p="%s",\
                destination_city="%s",destination_county="%s",\
                car_type="%s",cargo_type="%s",cargo_property="%s",\
                insurance="%s",cargo_volume="%s",cargo_weight="%s",\
                cargo_total_prices="%s",touch_phone="%s",\
                other_requests="%s",release_time="%s",end_time="%s"\
                 where id="%s";'
        mess = (message + '#' + id).split('#')
        try:                                 
            self.cursor.execute(sql % tuple(mess))
            self.db.commit()
        except:
            self.db.rollback()
            return 'NO'