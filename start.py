#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
from timeLog import Time
from dataHandleController import DataHandleController
from config import Config
t = Time()
config = Config()

while True:
	#the 3 vars following is a int.
	currentDay = t.getDay()
	currentMonth = t.getMonth()
	currentYear = t.getYear()
	if currentDay == 1:
	#if True:
		fileHandle = open ( '''logs/log%s.log'''%(t.getDate()), 'w' )  
		dhc = DataHandleController(currentDay,currentMonth,currentYear,fileHandle,config)
		dhc.startHandle()
		fileHandle.close()
		print '''today\'s job finished, sleep for another day.'''
		t.sleepDay(1)
	else:
		if currentMonth < 10:
			fileHandle = open ( '''logs/log%s-0%s-01.log'''%(currentYear,currentMonth), 'a' )
		else:
			fileHandle = open ( '''logs/log%s-%s-01.log'''%(currentYear,currentMonth), 'a' )  
		print '''today is %s,sleep for another day.'''%(t.toString())
		fileHandle.write ( '''today is %s,sleep for another day.'''%(t.toString()) ) 
		fileHandle.close()
		t.sleepDay(1)
	# # If there is sth. wrong, we can use following sentence to test.
	# fileHandle = open ( '''logs/log%s.log'''%(t.getDate()), 'w' )  
	# dhc = DataHandleController(currentDay,currentMonth,currentYear,fileHandle)
	# dhc.startHandle()
	# fileHandle.close()
	break
#author:zhuyifan



