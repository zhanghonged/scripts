#coding:utf-8

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendzl(mailacc,res_name,res_href):
    mail_from='233571510@qq.com'
    mail_to=[mailacc]
    mail_body='%s:%s'%(res_name,res_href)
    title='%s-积分兑换资料成功'%res_name
    msg=MIMEMultipart()
    body=MIMEText(mail_body,'plain','utf-8')
    msg.attach(body)

    msg['Subject']=title
    msg['From']=mail_from
    msg['To']=','.join(mail_to)

    try:
        server=smtplib.SMTP_SSL('smtp.qq.com',465)
        server.login(mail_from,'uzzlcwkjidifbidi')
        server.sendmail(mail_from,mail_to,msg.as_string())
        server.quit()
        print '邮件发送成功'
    except smtplib.SMTPException as e:
        print 'Error:邮件发送失败'
        print e