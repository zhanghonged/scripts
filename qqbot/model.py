#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-11 14:55:24
# @Author  : zhanghong (zhanghonged@126.com)
# @Link    : http://blog.codecp.org/
# @Version : $Id$

import peewee
import datetime


db=peewee.SqliteDatabase("bot.db")

class User(peewee.Model):
	
	name=peewee.CharField(max_length=32)
	qq=peewee.CharField(max_length=32)
	Qqtime=peewee.DateField()
	Num=peewee.IntegerField()
	Money=peewee.IntegerField()
	Nca=peewee.IntegerField()

	class Meta:
		database = db   #这个User模型使用"bot.db"数据库

class Resource(peewee.Model):
	name=peewee.CharField(max_length=32)
	href=peewee.CharField(max_length=32)
	Money=peewee.IntegerField()
	class Meta:
		database = db
if __name__ == '__main__':
	#User.create_table()
	#Resource.create_table()
	db.create_tables([User,Resource])
	
	# a=User.get(qq='2366651659')
	# a.Qqtime=a.Qqtime-datetime.timedelta(days=1)
	# print a.Qqtime
	# a.save()
