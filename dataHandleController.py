#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
from TVCalendar import TVCalendar
from database import Database

import sys
import string
import re
import time

class DataHandleController(object):
	def __init__(self, day, month, year,filehandler):
		#super(dataHandleController, self).__init__()
		self.day = day
		self.month = month
		self.year = year
		self.filehandler = filehandler
	def startHandle(self):
		reload(sys)
		sys.setdefaultencoding('utf-8') 

		print('NOTICE:Config loaded.')
		print('NOTICE:Start getting data from webside...')
		self.filehandler.write('NOTICE:Config loaded.\n')
		self.filehandler.write('NOTICE:Start getting data from webside...\n')

		tc = TVCalendar()
		tc_data1 = tc.toString()
		tc_data2 = {}
		if self.month == 12:
			tc_data2 = tc.toString(1,(self.year+1))
		else:
			tc_data2 = tc.toString((self.month+1),self.year)
		#tc_data= dict(tc_data1, **tc_data2)
		tc_data = [tc_data1,tc_data2]

		db = Database(self.filehandler)

		print('NOTICE:Data gathered successfully.')
		print('NOTICE:Start formatting data...')
		self.filehandler.write('NOTICE:Data gathered successfully.\n')
		self.filehandler.write('NOTICE:Start formatting data...\n')

		for td in tc_data:
			#make sure that all date are like dd-mm-yyyy
			keyToBeDel = []
			keyToBeAdd = []
			for key,value in td.iteritems():
				flagDelKey = False
				match = re.search(r'^[0-9]-\d+-[0-9][0-9][0-9][0-9]',key)
				if match:
					key_new = '0'+key
					flagDelKey = True
				else:
					key_new = key
				match_second = re.search(r'^[0-9][0-9]-[0-9]-[0-9][0-9][0-9][0-9]',key_new)
				if match_second:
					key_new_sec = key_new[0:3]+'0'+key_new[3:]
					flagDelKey = True
				else:
					pass
				if flagDelKey:
					keyToBeAdd.append(key_new_sec)
					keyToBeDel.append(key)
				else:
					pass
			for a in keyToBeAdd:
				d = keyToBeDel.pop()
				td[a] = td[d]
				del td[d]
			
			print('NOTICE:Data formatted successfully.')
			print('NOTICE:Start sorting data...')
			self.filehandler.write('NOTICE:Data formatted successfully.\n')
			self.filehandler.write('NOTICE:Start sorting data...\n')

			# Here is a test example, Dont remove it
			# for key,value in tc_data.iteritems():
			# 	print(key)
			# print('=============================')
			tc_sorted = sorted(td.iteritems(),key = lambda asd:asd[0] ,reverse = False)	#sorted by dictionary order
			# for key,value in tc_sorted:
			# 	print(key)

			print('NOTICE:Data sorted successfully.')
			print('NOTICE:Start saving data...')
			self.filehandler.write('NOTICE:Data sorted successfully.\n')
			self.filehandler.write('NOTICE:Start saving this month\'s data...\n')

			# Start to insert sth. into database
			for key,value in tc_sorted:
				# A module that check if the date has been already stored. If so, we will ignoire it.
				#print '''key=%s, value=%s'''%(key, value)
				#dateLastday is an array that contains 3 numbers(string) which means day, month and year.
				dateLastDay = db.getLastDay()[0].split('-')
				dayLastDay = string.atoi(dateLastDay[0])
				monthLastDay = string.atoi(dateLastDay[1])
				yearLastDay = string.atoi(dateLastDay[2])
				#print('''%s,%s,%s'''%(dayLastDay,monthLastDay,yearLastDay))

				#dateThisDay is similar to dateLastDay,but it means the record from web.
				dateThisDay = key.split('-')
				dayThisDay = string.atoi(dateThisDay[0])
				monthThisDay = string.atoi(dateThisDay[1])
				yearThisDay = string.atoi(dateThisDay[2])
				#print('''%s,%s,%s'''%(dayThisDay,monthThisDay,yearThisDay))

				#compare date and decide wether change the config lastday
				flagChangeDate = False
				if yearThisDay > yearLastDay:
					flagChangeDate = True
				elif yearThisDay == yearLastDay:
					if monthThisDay > monthLastDay:
						flagChangeDate = True
					elif monthThisDay == monthLastDay:
						if dayThisDay > dayLastDay:
							flagChangeDate = True
						else:
							pass
					else:
						pass
				else:
					pass

				if flagChangeDate:
					db.updateLastDay(key)
				else:
					print('''%s,%s,%s is too old.'''%(dayThisDay,monthThisDay,yearThisDay))
					self.filehandler.write('''NOTICE:%s,%s,%s is too old,ignore.\n'''%(dayThisDay,monthThisDay,yearThisDay))
					continue

				for aDay in value:
					n_id_rec = db.insertName(aDay['name'],'')
					dateThisDay = key.split('-')
					dateString = '''%s-%s-%s 00:00:00'''%(dateThisDay[2],dateThisDay[1],dateThisDay[0])
					if n_id_rec != "InsertError":
						n_id = n_id_rec[0]
						Insertstate = db.insertEpisode(n_id,aDay['season'],aDay['episode'],'',dateString,'')
						if Insertstate == "ok":
							print('''Insert-episode:%s,season:%s,episode:%s,day:%s'''%(aDay['name'],aDay['season'],aDay['episode'],key))
							self.filehandler.write('''NOTICE:Insert a record in Episode - name:%s,season:%s,episode:%s,day:%s\n'''%(aDay['name'],aDay['season'],aDay['episode'],key))
						else:
							print('An error in insert episode')
							self.filehandler.write('ERROR:An error in insert episode\n')
					else:
						print('An error in insert name')
						self.filehandler.write('ERROR:An error in insert name\n')
				print '--------------------------------'
				self.filehandler.write('-----------------------------\n')
		print('NOTICE:All data saved successfully.')
		self.filehandler.write('''NOTICE:On %s-%s-%s,data saved successfully.\n'''%(dateThisDay[2],dateThisDay[1],dateThisDay[0]))
		return True

#Author:zhuyifan on 12-5-2015 in Beijing
