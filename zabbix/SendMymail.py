#!/usr/bin/python
#coding:utf-8
import sys
import smtplib
from email.mime.text import MIMEText

mail_server = "smtp.exmail.qq.com"
mail_server_port = 465
mail_user = "xxxxxxxxx"
mail_passwd = "xxxxxxxxxxxxx"

class MyEmail:
    def __init__(self,to_list,subject,content):
        self.mail_server = mail_server
        self.mail_server_port = mail_server_port
        self.user = mail_user
        self.passwd = mail_passwd
        self.to_list = to_list
        self.subject = subject
        self.content = content

    def send(self):
        try:
            server = smtplib.SMTP_SSL(self.mail_server,self.mail_server_port)
            server.login(self.user, self.passwd)
            server.sendmail(self.user, self.to_list, self.get_attach())
            server.close()
            print("邮件发送成功")
            return True
        except Exception as e:
            print("邮件发送失败: %s" %str(e))
            return False

    def get_attach(self):
        attach = MIMEText(self.content,'plain','utf-8')
        attach["Subject"] = self.subject
        attach["From"] = "zabbix报警" + "<" + self.user + ">"
        attach["To"] = self.to_list
        return attach.as_string()

if __name__ == "__main__":
    my = MyEmail(sys.argv[1],sys.argv[2],sys.argv[3])
    my.send() 
