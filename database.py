#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb


#conn = MySQLdb.connect(host="localhost",user="root",passwd="123123",db="qiwsirtest",port=3306,charset="utf8")
class Database(object):
	def __init__(h,u,p,d,fileHandler):
		self.host = h
		self.user = u
		self.passwd = p
		self.db = d
		self.fileHandler = fileHandler
	def __init__(self,fileHandler,config):
		self.host = config.dataBaseHost
		self.user = config.dataBaseUser
		self.passwd = config.dataBasePwd
		self.db = config.dataBasedb
		self.fileHandler = fileHandler
	def connect(self):
		try:
			conn = MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,charset='utf8')
		except Exception, e:
			print(e)
			self.fileHandler.write(str(e))
			return "connectError"
		return conn
	def getAllNames(self):
		try:
			dbc = self.connect()
			cursor = dbc.cursor()
			sql = "select * from name"
			cursor.execute(sql)
			datas = cursor.fetchall()	
		except Exception, e:
			print(e)
			self.fileHandler.write(str(e))
			dbc.close()
			return "SelectError"
		#for data in datas:
		#	print(data)
		dbc.close()
		return datas
	def insertName(self,name,photoLink):
		db = self.connect()
		cursor = db.cursor()
		try:
			sql = '''insert into name(n_name,n_photoLink) values(\"%s\",\"%s\")'''%(name,photoLink)
			cursor.execute(sql)
			db.commit()
			self.fileHandler.write('''NOTICE: Insert a name:%s'''%(name))
			sql = '''select n_id from name where n_name = \"%s\"'''%(name)
			cursor.execute(sql)
			data = cursor.fetchone()
			db.close()
			return data
		except Exception, e:
			if e[0] == 1062: #means Duplicate entry
				sql = '''select n_id from name where n_name = \"%s\"'''%(name)
				cursor.execute(sql)
				data = cursor.fetchone()
				db.close()
				return data
			else:
				print(e)
				self.fileHandler.write(str(e))
    			db.rollback()
    			db.close()
    			return "InsertError"
    	
	def insertEpisode(self,n_id,e_season,e_espisode,e_name,e_onAir,e_descirption):
		db = self.connect()
		cursor = db.cursor()
		sql = '''insert into episode(n_id,e_season,e_episode,e_name,e_onAir,e_description) values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")'''%(n_id,e_season,e_espisode,e_name,e_onAir,e_descirption)
		try:
			cursor.execute(sql)
			db.commit()
		except Exception, e:
			if e[0] == 45001: #means tri_protect
				db.close()
				return "RecordProtect"
			else:
				print(e)
				self.fileHandler.write(str(e))
				db.rollback()
				db.close()
				return "InsertError"
		db.close()
		return "ok"
	def getLastDay(self):
		db = self.connect()
		cursor = db.cursor()
		sql = "select c_value from config where c_name = \"lastDay\" limit 1"
		try:
			cursor.execute(sql)
			data = cursor.fetchone()
		except Exception, e:
			print(e)
			self.fileHandler.write(str(e))
			db.close()
			return "SelectError"
		db.close()
		return data
	def updateLastDay(self,ld):
		db = self.connect()
		cursor = db.cursor()
		sql = "update config set c_value = \"%s\" where c_name = \"lastDay\""%(ld)
		try:
			cursor.execute(sql)
			db.commit()
		except Exception, e:
			print(e)
			self.fileHandler.write(str(e))
			db.rollback()
			db.close()
			return "UpdateError"
		db.close()
		return True
#Author:zhuyifan on 11-5-2015 in Beijing
		
