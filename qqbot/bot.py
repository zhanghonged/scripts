#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-11 14:58:45
# @Author  : zhanghong (zhanghonged@126.com)
# @Link    : http://blog.codecp.org/
# @Version : $Id$

import qqbot
import datetime
from model import User, Resource
from botmail import sendzl
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


@qqbot.QQBotSlot
def onQQMessage(bot, contact, member, content):
    qqname = member.name
    qq = member.qq
    if "@ME" in content:
        print 'content:', content  # 内容
        print 'memeber:', member  # qq号
        print 'contact:', contact  # 群号
        if "签到" in content:
            try:
                user = User.get(qq=qq)
            except:
                user = User()
                user.qq = qq
                user.name = qqname
                user.Qqtime = datetime.date.today()
                user.Num = 1
                user.Money = 2
                user.Nca = 1
                user.save()
                sendData = '恭喜%s[%s]第一次签到成功，获得2积分，连续签到%s次' % (qqname, qq, user.Nca)
            else:
                nexttime = user.Qqtime
                nowtime = datetime.date.today()
                yesterdaytime = nowtime - datetime.timedelta(days=1)
                if nexttime == nowtime:
                    sendData = '%s[%s]今天已经签到过' % (qqname, qq)
                else:
                    user.Qqtime = nowtime
                    user.Num += 1
                    user.Money += 2
                    if nexttime == yesterdaytime:
                        user.Nca += 1
                    else:
                        user.Nca = 1
                    user.save()
                    sendData = '恭喜%s[%s]第%s签到成功，当前积分%s,连续签到%s次' % (qqname, qq, user.Num, user.Money, user.Nca)
            finally:
                bot.SendTo(contact, sendData)

        elif '查询' in content:
            data=Resource.select()
            res_list=['%s  %s  %s'%(i.id,i.name,i.Money) for i in data]
            res_list.insert(0,'ID  名称  积分')
            res_list.insert(0, '%s[%s]查询内容:' % (qqname,qq))
            sendData='\n'.join(res_list)
            bot.SendTo(contact, sendData)

        elif '兑换' in content:
            try:
                user = User.get(qq=qq)
            except:
                sendData='%s[%s]没有签到记录，不能兑换'%(qqname,qq)
            else:
                try:
                    data = Resource.get(id=int(content[-1]))
                except:
                    sendData = '%s[%s]兑换失败，ID:%s不存在' % (qqname, qq, content[-1])
                else:

                    if user.Money >= data.Money:
                        user.Money -= data.Money
                        user.save()
                        sendData = '%s[%s]兑换成功。\n%s已发送至您qq邮箱。' % (qqname, qq, data.name)
                        tmail=qq+'@qq.com'
                        sendzl(tmail,data.name,data.href)
                    else:
                        sendData = '%s[%s]兑换失败，积分不足' % (qqname, qq)
            finally:
                bot.SendTo(contact, sendData)


if __name__ == '__main__':
    qqbot.RunBot(qq="233571510")