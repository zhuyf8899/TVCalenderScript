#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
from TVCalendar import TVCalendar
from database import Database

import sys
reload(sys)
sys.setdefaultencoding('utf-8') 
#def application(env, start_response):
#	start_response('200 OK', [('Content-Type','text/html')])
#	tc = TVCalendar()
#	return [tc.outJson()]
#def printToScreen():
tc = TVCalendar()
#db = Database()
#db.insertName("ruby","http://img2.imgtn.bdimg.com/it/u=2216592883,259451779&fm=21&gp=0.jpg")
#db.insertEpisode("1","1","4","java-insert-4","2015-05-07 00:00:00","blabla")

print(tc.toString())
#print(tc.outJson())
