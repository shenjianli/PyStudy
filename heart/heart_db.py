#!/usr/bin/python3
# -*- coding:utf-8 -*-
import time
import pymysql


class HeartDB(object):
    def __init__(self):
        self.db = pymysql.connect(host="127.0.0.1", user="root", passwd="shen111111", db="heart")
        self.db.set_charset('utf8')
        self.cursor = self.db.cursor()

    # 打开数据库
    def open_db(self):
        self.db = pymysql.connect(host="127.0.0.1", user="root", passwd="shen111111", db="heart")
        self.db.set_charset('utf8')
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()

    # 查看mysql版本号
    def select_mysql_version(self):

        # 使用 execute()  方法执行 SQL 查询
        self.cursor.execute("SELECT VERSION()")

        # 使用 fetchone() 方法获取单条数据.
        data = self.cursor.fetchone()

        print("Database version : %s " % data)
        # 关闭数据库连接
        return data

    # 创建heart表
    def create_mysql_table(self):
        # 使用 execute() 方法执行 SQL，如果表存在则删除
        self.cursor.execute("DROP TABLE IF EXISTS heart")

        # 使用预处理语句创建表
        sql = """CREATE TABLE heart(heart_id BIGINT primary key AUTO_INCREMENT NOT NULL, heart_net_site CHAR(150), 
        heart_content TEXT, heart_date CHAR(20), type int default 0) DEFAULT CHARSET = utf8 """
        try:
            self.cursor.execute(sql)
            print("创建表成功")
        except:
            self.db.rollback()
            print("创建表失败")

    # 关闭数据库
    def close_joke_db(self):
        self.cursor.close()
        self.db.close

    # 向数据库中插入
    def insert_mysql_data(self, site, content):

        datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # SQL 插入语句
        sql = """INSERT INTO heart(heart_net_site,heart_content, heart_date) VALUES ('%s', '%s', '%s') """
        try:
            # 执行sql语句
            self.cursor.execute(sql % (site, content, datetime))
            # 提交到数据库执行
            self.db.commit()
            print("success")
        except Exception:
            # 如果发生错误则回滚
            self.db.rollback()
            print("fail")

    # 关闭数据库连接

    # 查询所有heart数据，返回json字符串
    def query_mysql_data(self):
        data_list = []
        data_item = {}
        # SQL 查询语句
        sql = "SELECT * FROM heart"
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            for row in results:
                heart_data = {}
                _id = row[0]
                heart_data['id'] = _id
                _site = row[1]
                heart_data['site'] = _site
                _content = row[2]
                if '<BR>' in _content:
                    _content = _content.replace("<BR>", "\n")
                heart_data['content'] = _content
                _date = row[3]
                heart_data['date'] = _date
                _type = row[4]
                heart_data['type'] = _type
                data_list.append(heart_data)
                # 打印结果
                print("id=%d,site=%s,content=%s,date=%s,type=%d" % (_id, _site, _content, _date, _type))
            data_item['code'] = 1
            data_item['msg'] = '查询成功'
            data_item['data'] = data_list
        except:
            print("Error: unable to fetch data")
        return data_item

    # 查询笑话数据，返回json字符串
    def query_mysql_data_limit_num(self, start_id, num):
        data_list = []
        data_item = {}
        # SQL 查询语句
        sql = "select * from heart where type = 0 and heart_id > %d ORDER BY heart_id * 1 ASC  limit %d"
        try:
            # 执行SQL语句
            self.cursor.execute(sql % (start_id, num))
            # 获取所有记录列表
            results = self.cursor.fetchall()
            for row in results:
                joke_data = {}
                joke_id = row[0]
                joke_data['id'] = joke_id
                joke_site = row[1]
                joke_data['site'] = joke_site
                joke_content = row[2]
                if '<BR>' in joke_content:
                    joke_content = joke_content.replace("<BR>", "\n")
                joke_data['content'] = joke_content
                joke_date = row[3]
                joke_data['date'] = joke_date
                _type = row[4]
                joke_data['type'] = _type
                data_list.append(joke_data)
                # 打印结果
                print("id=%d,site=%s,content=%s,date=%s,type=%d" % (joke_id, joke_site, joke_content, joke_date, _type))
            data_item['code'] = 1
            data_item['msg'] = '查询成功'
            data_item['data'] = data_list
        # joke_item['jokes'] = joke_list
        except:
            print("Error: unable to fetch data")
            data_item['code'] = -1
            data_item['msg'] = '服务器异常'
            data_item['data'] = data_list
        # joke_item['jokes'] = joke_list
        return data_item

    def fetch_data_num(self, num):
        data_list = []
        data_item = {}
        # SQL 查询语句
        sql = "select * from heart where type = 0 ORDER BY heart_id * 1 ASC  limit %d"
        try:
            # 执行SQL语句
            self.cursor.execute(sql % num)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            for row in results:
                joke_data = {}
                joke_id = row[0]
                joke_data['id'] = joke_id
                joke_site = row[1]
                joke_data['site'] = joke_site
                joke_content = row[2]
                if '<BR>' in joke_content:
                    joke_content = joke_content.replace("<BR>", "\n")
                joke_data['content'] = joke_content
                joke_date = row[3]
                joke_data['date'] = joke_date
                _type = row[4]
                joke_data['type'] = _type
                data_list.append(joke_data)
                # 打印结果
                print("id=%d,site=%s,content=%s,date=%s,type=%d" % (joke_id, joke_site, joke_content, joke_date, _type))
            data_item['code'] = 1
            data_item['msg'] = '查询成功'
            data_item['data'] = data_list
        # joke_item['jokes'] = joke_list
        except:
            print("Error: unable to fetch data")
            data_item['code'] = -1
            data_item['msg'] = '服务器异常'
            data_item['data'] = data_list
        # joke_item['jokes'] = joke_list
        return data_item

    # 查询heart数据，返回json字符串
    def query_heart_data_by_id(self, _id):
        data_list = []
        data_item = {}
        # SQL 查询语句
        sql = "select * from heart WHERE heart_id = %d"
        try:
            # 执行SQL语句
            self.cursor.execute(sql % _id)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            for row in results:
                heart_data = {}
                joke_id = row[0]
                heart_data['id'] = joke_id
                joke_site = row[1]
                heart_data['site'] = joke_site
                joke_content = row[2]
                if '<BR>' in joke_content:
                    joke_content = joke_content.replace("<BR>", "\n")
                heart_data['content'] = joke_content
                joke_date = row[3]
                heart_data['date'] = joke_date
                _type = row[4]
                heart_data['type'] = _type
                data_list.append(heart_data)
                # 打印结果
                print("id=%d,site=%s,content=%s,date=%s" % (joke_id, joke_site, joke_content, joke_date))
            data_item['code'] = 1
            data_item['msg'] = '查询成功'
            data_item['data'] = data_list
        except:
            print("Error: unable to fetch data")
            data_item['code'] = -1
            data_item['msg'] = '服务器异常'
            data_item['data'] = data_list
        return data_item

    # 查询数目
    def query_heart_data_count(self):
        # SQL 查询语句
        sql = "select COUNT(*) from heart where type = 0"
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            result = self.cursor.fetchall()
            count = int(result[0][0])
        except:
            print("Error: unable to fetch data")
        return count

    # 表示看过并且喜欢
    def update_heart_like(self, id):
        sql = "update heart set type = 1 where heart_id = %d"
        try:
            # 执行SQL语句
            self.cursor.execute(sql % id)
            result = self.db.commit()
            print(result)
        except:
            print("Error update fail ")

    # 表示显示看过
    def update_heart_look(self, id):
        sql = "update heart set type = -1 where heart_id = %d"
        try:
            # 执行SQL语句
            self.cursor.execute(sql % id)
            self.db.commit()
            print("更新发送状态 type 为 -1")
        except:
            print("Error update fail ")

    def delete_db_data(self):
        sql = "delete from heart"
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            self.db.commit()
            print("删除数据执行完成")
        except:
            print("Error update fail ")


# 主方法
if __name__ == '__main__':
    heartDb = HeartDB()

    version = heartDb.select_mysql_version()
    print("Database mysql : %s " % version)

    # heartDb.create_mysql_table()
    # heartDb.update_heart_like(2)
    # print(heartDb.query_heart_data_count())
    # print(heartDb.query_mysql_data())
    # print(heartDb.query_heart_data_by_id(1))
    print(heartDb.query_mysql_data_limit_num(1, 3))
    # insert_mysql_data("www.baidu.com","百度一下，就知道")
    # joke = query_mysql_data()
    # joke_json = json.dumps(joke,ensure_ascii=False)
    # print(joke_json)
    # close_joke_db()
