#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-11 14:58:45
# @Author  : zhanghong (zhanghonged@126.com)
# @Link    : http://blog.codecp.org/
# @Version : $Id$

import qqbot
import datetime
from model import User



@qqbot.QQBotSlot
def onQQMessage(bot,contact,member,content):
	qqname=member.name
	qq=member.qq
	if "@ME" in content:
		print 'content:',content #内容
		print 'memeber:',member  #qq号
		print 'contact:',contact #群号
		if "签到" in content:
			try:
				user=User.get(qq=qq)
			except:
				user=User()
				user.qq=qq
				user.name=qqname
				user.Qqtime=datetime.date.today()
				user.Num=1
				user.Money=2
				user.Nca=1
				user.save()
				sendData='恭喜%s[%s]第一次签到成功，获得2积分，连续签到%s次'%(qqname,qq,user.Nca)
			else:
				nexttime=user.Qqtime
				nowtime=datetime.date.today()
				yesterdaytime = nowtime - datetime.timedelta(days=1)
				print 'nexttime:',nexttime
				print 'nowtime:',nowtime
				print 'yesterdaytime:',yesterdaytime
				if nexttime == nowtime:
					sendData='%s[%s]今天已经签到过'%(qqname,qq)
				else:
					user.Qqtime=nowtime
					user.Num+=1
					user.Money+=2
					if nexttime == yesterdaytime:
						user.Nca += 1
					else:
						user.Nca = 1
					user.save()
					sendData='恭喜%s[%s]第%s签到成功，当前积分%s,连续签到%s次'%(qqname,qq,user.Num,user.Money,user.Nca)
			finally:
				bot.SendTo(contact,sendData)

if __name__ == '__main__':
	qqbot.RunBot(qq="233571510")