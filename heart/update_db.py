#!/usr/bin/python3
# -*- coding:utf-8 -*-
import time
import pymysql


class UpdateDB(object):
	def __init__(self):
		self.db = pymysql.connect(host="127.0.0.1", user="root", passwd="shen111111", db="heart")
		self.db.set_charset('utf8')
		self.cursor = self.db.cursor()

	# 打开数据库
	def open_db(self):
		# 打开数据库连接
		self.db = pymysql.connect(host="127.0.0.1", user="root", passwd="shen111111", db="heart")
		self.db.set_charset('utf8')
		# 使用 cursor() 方法创建一个游标对象 cursor
		self.cursor = self.db.cursor()

	def create_mysql_table(self):
		# 使用 execute() 方法执行 SQL，如果表存在则删除
		self.cursor.execute("drop table if exists heart_history")

		# 使用预处理语句创建表
		sql = """create table heart_history (history_id BIGINT primary key AUTO_INCREMENT  NOT NULL ,history_net_site  
		CHAR(150),history_date CHAR(20), last_page_num int default 1) DEFAULT CHARSET=utf8 """

		try:
			self.cursor.execute(sql)
			print("创建表成功")
		except:
			self.db.rollback()
			print("创建表失败")

	def close_joke_db(self):
		self.cursor.close()
		self.db.close

	def insert_mysql_data(self, site, page_num):

		datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

		# SQL 插入语句
		sql = """INSERT INTO heart_history(history_net_site,history_date,last_page_num) VALUES ('%s', '%s','%d') """
		try:
			# 执行sql语句
			self.cursor.execute(sql % (site, datetime, page_num))
			# 提交到数据库执行
			self.db.commit()
			print("success")
		except Exception:
				# 如果发生错误则回滚
			self.db.rollback()
			print("fail")

	def query_mysql_data(self):
		result = 1
		# SQL 查询语句
		sql = "SELECT * FROM heart_history ORDER BY history_id DESC"
		try:
			# 执行SQL语句
			self.cursor.execute(sql)
			# 获取所有记录列表
			results = self.cursor.fetchall()
			if len(results) != 0:
				history = results[0]
				if len(history) != 0:
					result = int(history[3])
		except:
			print("Error: unable to fetch data")
		return result

	def is_exit_table(self):
		sql = "SELECT * FROM information_schema.tables WHERE table_name = '%s'"
		# 执行SQL语句
		self.cursor.execute(sql % 'heart_history')
		# 获取所有记录列表
		results = self.cursor.fetchall()
		if 'heart_history' in results:
			print("已经存在数据表")
		else:
			print("不存在数据表")

	def delete_db_data(self):
		sql = "delete from heart_history"
		try:
			# 执行SQL语句
			self.cursor.execute(sql)
			self.db.commit()
			print("删除数据执行完成")
		except:
			print("Error update fail ")


if __name__ == '__main__':

	updateDb = UpdateDB()
	# updateDb.create_mysql_table()
	print(updateDb.query_mysql_data())
	# insert_mysql_data("www.baidu.com","百度一下，就知道")
	# joke = query_mysql_data()
	# joke_json = json.dumps(joke,ensure_ascii=False)
	# print(joke_json)
	# close_joke_db()
	#insert_mysql_data('/jokehtml/冷笑话/201709082323108.htm')
	#is_exit_table()