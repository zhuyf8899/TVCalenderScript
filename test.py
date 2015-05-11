#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
from TVCalendar import TVCalendar
from database import Database

import sys
import string
import re
reload(sys)
sys.setdefaultencoding('utf-8') 

print('NOTICE:Config loaded.')
print('NOTICE:Start getting data from webside...')

tc = TVCalendar()
tc_data = tc.toString()
db = Database()

print('NOTICE:Data gathered successfully.')
print('NOTICE:Start formatting data...')

#make sure that all date are like dd-mm-yyyy
keyToBeDel = []
keyToBeAdd = []
for key,value in tc_data.iteritems():
	flagDelKey = False
	match = re.search(r'^[0-9]-\d+-[0-9][0-9][0-9][0-9]',key)
	if match:
		key_new = '0'+key
		flagDelKey = True
		# tc_data[key_new] = tc_data[key]
		# del tc_data[key]
	else:
		key_new = key
	match_second = re.search(r'^[0-9][0-9]-[0-9]-[0-9][0-9][0-9][0-9]',key_new)
	if match_second:
		key_new_sec = key_new[0:3]+'0'+key_new[3:]
		flagDelKey = True
	else:
		pass
	if flagDelKey:
		#tc_data[key_new_sec] = tc_data[key]
		keyToBeAdd.append(key_new_sec)
		keyToBeDel.append(key)
	else:
		pass
for a in keyToBeAdd:
	d = keyToBeDel.pop()
	tc_data[a] = tc_data[d]
	del tc_data[d]

print('NOTICE:Data formatted successfully.')
print('NOTICE:Start sorting data...')

# Here is a test example, Dont remove it
# for key,value in tc_data.iteritems():
# 	print(key)
# print('=============================')
tc_sorted = sorted(tc_data.iteritems(),key = lambda asd:asd[0] ,reverse = False)	#sorted by dictionary order
# for key,value in tc_sorted:
# 	print(key)

print('NOTICE:Data sorted successfully.')
print('NOTICE:Start saving data...')

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
		continue

	for aDay in value:
		n_id_rec = db.insertName(aDay['name'],'')
		dateThisDay = key.split('-')
		dateString = '''%s-%s-%s 00:00:00'''%(dateThisDay[2],dateThisDay[1],dateThisDay[0])
		if n_id_rec != "InsertError":
			n_id = n_id_rec[0]
			Insertstate = db.insertEpisode(n_id,aDay['season'],aDay['episode'],'',dateString,'')
			if Insertstate == "ok":
				print('''Insert-name:%s,season:%s,episode:%s,day:%s'''%(aDay['name'],aDay['season'],aDay['episode'],key))
			else:
				print('An error in insert episode')
		else:
			print('An error in insert name')
	print '--------------------------------'
print('NOTICE:Data saved successfully.')
