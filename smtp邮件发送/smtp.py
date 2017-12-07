#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-16 16:32:39
# @Author  : zhanghong (zhanghonged@126.com)
# @Link    : http://blog.codecp.org/
# @Version : $Id$

import smtplib
import time
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import Encoders


#发信邮箱 
mail_from='233571510@qq.com'
#收信邮箱 
mail_to=['zhanghong@16feng.com']
#正文
mail_body='附件是smtplib模块的相关操作截图，发邮件以做备份。'

mail_body_html='''
				<html>
				<body>
				<h1>教程smtplib模块截图</h1>
				<p><img src="cid:image1"></p>
				</body>
				</html>
			'''

#标题
title='教程smtplib模块截图'

#发送带附件的邮件

# 构造MIMEMultipart对象做为根容器
msg=MIMEMultipart()
# 构造MIMEText对象做为邮件显示内容并附加到根容器
# 可以发送纯文本格式和html格式两种
# body=MIMEText(mail_body,'plain','utf-8')
# msg.attach(body)

body_html=MIMEText(mail_body_html,'html','utf-8')
msg.attach(body_html)

# 附件先添加一个压缩包文件
# 构造MIMEBase对象做为文件附件内容并附加到根容器
rar_part=MIMEBase('application','octet-stream')
# 读入文件内容并格式化
rar_part.set_payload(open('C:\\Users\\zhanghong\\Desktop\\mail.rar','rb').read())
Encoders.encode_base64(rar_part)
rar_part.add_header('Content-Disposition','attachment',filename='mail.rar')
msg.attach(rar_part)

# 添加一个图片附件
img_part=MIMEBase('application','octet-stream')
img_part.set_payload(open('C:\\Users\\zhanghong\\Desktop\\mail\\3.png','rb').read())
Encoders.encode_base64(img_part)
img_part.add_header('Content-Disposition','attachment',filename='3.png')
img_part.add_header('Content-ID', '<image1>')
msg.attach(img_part)

# 添加一个office附件
office_part=MIMEBase('application','octet-stream')
office_part.set_payload(open('C:\\Users\\zhanghong\\Desktop\\三期功能计划.xlsx'.decode('utf-8'),'rb').read())
Encoders.encode_base64(office_part)
#注意：此处filename要转换为gb2312编码，否则中文会有乱码。  
#      特别，此处的filename为unicode编码，所以可以用basename.encode('gb2312')  
#            如果filename为utf-8编码，要用basename.decode('utf-8').encode('gb2312)
office_part.add_header('Content-Disposition','attachment',filename='三期功能计划.xlsx'.decode('utf-8').encode('gb2312'))
msg.attach(office_part)

#定义标题
msg['Subject']=title
#定义发件人
msg['From']=mail_from
#定义收件人
msg['To']=','.join(mail_to)
#定义发送时间（不定义的可能有的邮件客户端会不显示发送时间） 
msg['date']=time.strftime('%a, %d %b %Y %H:%M:%S %z')

try:
	server=smtplib.SMTP_SSL('smtp.qq.com',465)
	#设置是否为调试模式。默认为False，即非调试模式，表示不输出任何调试信息。
	#server.set_debuglevel(1)
	server.login(mail_from,'xenvilsuelidbhii')
	server.sendmail(mail_from,mail_to,msg.as_string())
	server.quit()
	print '邮件发送成功'
except smtplib.SMTPException:
	print 'Error:邮件发送失败'
