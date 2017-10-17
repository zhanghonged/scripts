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
		print content #内容
		print member  #qq号
		print contact #群号
		if 'hello' in content:
			sendData="""
				/疑问/疑问/疑问/疑问
				啥情况？
				/疑问/疑问/疑问/疑问
			"""
			bot.SendTo(contact,sendData)

		elif "签到" in content:
			try:
				user=User.get(qq=qq)
			except:
				user=User()
				user.qq=qq
				user.name=qqname
				user.Qqtime=datetime.datetime.now()
				user.Num=1
				user.Money=2
				user.save()
				sendData="""
					恭喜%s[%s]第一次签到成功，获得2积分
				"""%(qqname,qq)
			else:
				nexttime=user.Qqtime.strftime("%y-%m-%d")
				nowtime=datetime.datetime.now().strftime("%y-%m-%d")
				if nexttime == nowtime:
					sendData="""
						%s[%s]已经签到过
					"""%(qqname,qq)
				else:
					user.Qqtime=datetime.datetime.now()
					user.Num+=1
					user.Money+=2
					user.save()
					sendData="""
						恭喜%s[%s]第%签到成功，当前积分%s
					"""%(qqname,qq,user.Num,user.Money)
			finally:
				bot.sendData(contact,sendData)		

if __name__ == '__main__':
	qqbot.RunBot(qq="233571510")