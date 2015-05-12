# TVCalenderShell
a TVCalender shell script to get data automaticly 
### Attention: this repository is under construction
####0.What we need is following:
#####	0.1 LAMP:ubuntu1404,Apache,Mysql,php

#####	0.2 python BeautifulSoap4:
			<pre><code>sudo apt-get install python-bs4</code></pre>
#####	0.3 python MySQLdb: sudo apt-get install python-mysqldb
			<pre><code>sudo apt-get install python-mysqldb</code></pre>
#####	0.4 a Mysql database named as 'tcdb', then we put the tcdb.sql into the database(trigger included).

#####	0.5 set timezone and sync the time:
			<pre><code>sudo ntpdate s1b.time.edu.cn</br>
						sudo hwclock --systohc</code></pre>
#####	0.6 in database tcdb, a record must be inserted into table config: 
			<pre><code>insert into config (c_name,c_value) values ("lastDay","30-04-2015");</code></pre>
####1.the first step of this script is to get whole HTML page from a specfic page and get some info:
#####	1.1 The organization of the json is like below:
>		{"date":[{"season":"","episode":"","name":""},{"seasonAnother":"","episodeAnother":"","nameAnother":""},...],"dateAnother":[...],...}
		Which also means a dictionary that contains all dates in this month, for each key and value is a array consists of dictionaries of each episode on air that day.

#####	1.2 The module database is used to do something with the MySQL database:
######		1.2.1 It can conenct the database by method connect. In this method, all config can be setted by __init__, but there is a default config due to laziness of author.
######		1.2.2 Also,when this scirpt get some names of TV dramas, it firstly insert the name into table "name". Of course the name is unique for this time so don't worry if we insert something when the table has had them.
######		1.2.3 There is a trigger called tri_InsertProtect on table episode, which is used to forbid script inserting a record with same TV drama name, same season, same episode， same on air time.

#####	1.3 The python script consists of 3 modules: 
######		1.3.1 TVCalendar -- get data from webside http://www.pogdesign.co.uk/cat/. However this module works well without checking any mistakes, I will update ASAP(Of course this module is finished by Gaoming, not me.)
######		1.3.2 Database -- make data store into database correctlly.
######		1.3.3 Main test -- we start it to do all the work.

ps. This work is a module of TVCledner Project, this project is leaded by Gaoming, it is also a product of GaoMing Special Group in <a href='http://iflab.org'>ifLab.org</a>