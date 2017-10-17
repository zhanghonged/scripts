#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-11 14:55:24
# @Author  : zhanghong (zhanghonged@126.com)
# @Link    : http://blog.codecp.org/
# @Version : $Id$

import peewee

db=peewee.SqliteDatabase("bot.db")

class User(peewee.Model):
	
	name=peewee.CharField(max_length=32)
	qq=peewee.CharField(max_length=32)
	Qqtime=peewee.DateField()
	Num=peewee.IntegerField()
	Money=peewee.IntegerField()

	class Meta:
		database = db
if __name__ == '__main__':
	User.create_table()