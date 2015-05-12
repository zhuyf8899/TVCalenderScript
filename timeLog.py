#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import time

import string

class Time(object):
	"""a module to meature time"""
	def __init__(self):
		pass
	def getDay(self):
		return string.atoi(time.strftime("%d",time.localtime(time.time())))
	def getMonth(self):
		return string.atoi(time.strftime("%m",time.localtime(time.time())))
	def getYear(self):
		return string.atoi(time.strftime("%Y",time.localtime(time.time())))
	def toString(self):
		return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
	def sleepDay(self,days):
		time.sleep(60*60*24*days)
		return True
	def getDate(self):
		return time.strftime("%Y-%m-%d",time.localtime(time.time()))

