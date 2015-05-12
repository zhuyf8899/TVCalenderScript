#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import urllib  
import urllib2
import cookielib
import re
from bs4 import BeautifulSoup
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class TVCalendar:
    def __init__(self, username = '', password = ''):
        self.username = username
        self.password = password
        self.data = {}

    def getData(self,month = '',year = ''):
        #month should be like m-yyyy,the month shouldn't have 0
        cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        postdata=urllib.urlencode({
            'username': self.username, 
            'password': self.password, 
            'sub_login':'Account Login'
        })
        if (month != '') and (year != ''):
            strPara = str(month) + '-' + str(year)
        else:
            strPara = ''
        req = urllib2.Request(
            url = 'http://www.pogdesign.co.uk/cat/'+ strPara, 
            data = postdata
        )
        htmlData = ""
        htmlData = opener.open(req).read() #获取网页原始数据
        if htmlData:
            for dayHtml in BeautifulSoup(htmlData).findAll('td', attrs={'class' : 'day'}) : #对网页原始数据进行解析，并进行按日分割
                date = re.search('\d{1,2}-\d{1,2}-\d{4}', str(dayHtml)) #获取日期
                episodes = []
                for episodeData in re.findall('[^/]+/Season-\d{1,2}/Episode-\d{1,2}', str(dayHtml)) : #获取剧集
                    episodeList = re.split('/', str(episodeData))
                    episode = {'name' : episodeList[0], 
                               'season' : re.search('\d{1,2}',str(episodeList[1])).group(), 
                               'episode' : re.search('\d{1,2}',str(episodeList[2])).group()}
                    episodes.append(episode)
                self.data[str(date.group())] = episodes
            return True
        else :
            return False

    def outJson(self):
        if self.data:
            return json.dumps(self.data)
        else :
            if self.getData():
                return json.dumps(self.data)
            else :
                return None
    def toString(self,month = '',year = ''):
        self.data = {}
        if self.getData(month,year):
            return self.data
        else:
            return None
#original author: Gaoming
#edited by zhuyifan 