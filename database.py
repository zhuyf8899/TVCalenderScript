#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb


#conn = MySQLdb.connect(host="localhost",user="root",passwd="123123",db="qiwsirtest",port=3306,charset="utf8")
class Database(object):
	def __init__(h,u,p,d):
		self.host = h
		self.user = u
		self.passwd = p
		self.db = d
	def __init__(self):
		self.host = "localhost"
		self.user = "root"
		self.passwd = "ubuntu1404"
		self.db = "tcdb"
	def connect(self):
		try:
			conn = MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,charset='utf8')
		except Exception, e:
			print(e)
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
			return "SelectError"
		#for data in datas:
		#	print(data)
		dbc.close
		return datas
	def insertName(self,name,photoLink):
		try:
			db = self.connect()
			cursor = db.cursor()
			sql = '''insert into name(n_name,n_photoLink) values(\"%s\",\"%s\")'''%(name,photoLink)
			cursor.execute(sql)
			db.commit()
		except Exception, e:
			print(e)
    		db.rollback()
    		return "InsertError"
		db.close
	def insertEpisode(self,n_id,e_season,e_espisode,e_name,e_onAir,e_descirption):
		db = self.connect()
		cursor = db.cursor()
		sql = '''insert into episode(n_id,e_season,e_episode,e_name,e_onAir,e_description) values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")'''%(n_id,e_season,e_espisode,e_name,e_onAir,e_descirption)
		print(sql)
		try:
			cursor.execute(sql)
			db.commit()
		except Exception, e:
			print(e)
			db.rollback()
			return "InsertError"
		db.close()
