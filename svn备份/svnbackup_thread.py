#coding:utf-8

import os
import threading
import datetime
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

##发件相关设置
issendmail=True
mail_from = '233571510@qq.com'
mail_passwd='xxxxxxxxxx'
mail_smtp='smtp.qq.com'
mail_smtp_port=465
mail_to = ['zhanghong@16feng.com','shemq@16feng.com']

##需要备份的版本库
repos=['fx','Abc','it','yiren','5ecat','icoffer']
svn_reporoot=r'E:\Repositories'
svn_bakroot=r'E:\bak'

def sendmail(title,mail_body):
    msg=MIMEMultipart()
    body = MIMEText(mail_body, 'plain', 'utf-8')
    msg.attach(body)
    msg['Subject'] = title
    msg['from'] = mail_from
    msg['to'] = ','.join(mail_to)
    try:
        server = smtplib.SMTP_SSL(mail_smtp, mail_smtp_port)
        server.login(mail_from, mail_passwd)
        server.sendmail(mail_from, mail_to, msg.as_string())
        server.quit()
        print '邮件发送成功'
    except smtplib.SMTPException as e:
        print e
        print '邮件发送失败'

def decorator(fun):
    def wrapper(self):
        result=fun(self)[self.repo]
        RecordVersion_file = '%s%s%s%s%s_LastRevision.txt' % (svn_bakroot, os.sep, self.repo, os.sep, self.repo)
        Log_file = '%s%s%s%s%s_log.txt' % (svn_bakroot, os.sep, self.repo, os.sep, self.repo)
        if result['result'] == '备份成功':
            print '%s 备份成功，记录这次备份的版本号%s' % (self.repo,result['CurrentNum'])
            with open(RecordVersion_file,'wb') as f:
                f.write(result['CurrentNum'])
            print '%s 开始记录log'%self.repo
            with open(Log_file,'ab+')as f:
                f.write(str(datetime.datetime.now()))
                f.write('  -- 添加备份文件 %s，从[%s]到[%s]。'%(result['DumpFile'],result['StartNum'],result['CurrentNum'])+'\n')

            title='svn版本库%s备份成功%s_%s'%(self.repo,result['StartNum'],result['CurrentNum'])
            mail_body='Svn版本库%s备份成功：\n版本库：%s\n备份时间：%s\n版本号：[%s]_[%s]'%(self.repo,self.repo,datetime.datetime.now(),result['StartNum'],result['CurrentNum'])
        elif result['result'] == '版本库不存在':
            print '%s版本库不存在,无需备份!'%self.repo
            title = 'svn版本库%s备份未进行' %self.repo
            mail_body = 'Svn版本库%s备份未进行：\n版本库：%s\n时间：%s\n未进行原因：%s' % (self.repo,self.repo,datetime.datetime.now(),result['result'])
        elif result['result'] == '版本库为空':
            print '%s版本库为空,无需备份!'%self.repo
            title = 'svn版本库%s备份未进行' %self.repo
            mail_body = 'Svn版本库%s备份未进行：\n版本库：%s\n时间：%s\n未进行原因：%s' % (self.repo,self.repo,datetime.datetime.now(),result['result'])
        elif result['result'] == '版本未增加':
            print '%s版本未增加,无需备份!'%self.repo
            title = 'svn版本库%s备份未进行' %self.repo
            mail_body = 'Svn版本库%s备份未进行：\n版本库：%s\n时间：%s\n未进行原因：%s' % (self.repo,self.repo,datetime.datetime.now(),result['result'])
        else:
            print '%s版本库备份失败!'
            title = 'svn版本库%s备份失败' % (self.repo)
            mail_body = 'Svn版本库%s备份失败：\n版本库：%s\n时间：%s\n版本号：[%s]_[%s]\n失败原因：%s' % (self.repo,self.repo,datetime.datetime.now(),result['StartNum'],result['CurrentNum'],result['result'])
        if issendmail == True:
            sendmail(title,mail_body)
    return wrapper


class Svnbak(threading.Thread):
    def __init__(self,repo,rv):
        self.repo=repo
        self.svn_reporoot=svn_reporoot
        self.svn_bakroot=svn_bakroot
        self.RecordVersion_file='%s%s%s%s%s_LastRevision.txt' %(svn_bakroot,os.sep,self.repo,os.sep,self.repo)
        self.CurrentNum=os.popen('svnlook youngest %s/%s'%(svn_reporoot,self.repo)).read().strip()
        self.StartNum=0
        self.rv=rv
        self.rv[self.repo]={}
        threading.Thread.__init__(self)

    @decorator
    def run(self):
        if self.CurrentNum:
            if int(self.CurrentNum) > 0:
                try:
                    with open(self.RecordVersion_file, 'rb') as f:
                        self.StartNum=int(f.read())+1
                except:
                    self.StartNum=0
                    if not os.path.isdir('%s%s%s' % (self.svn_bakroot, os.sep, self.repo)):
                        os.makedirs('%s%s%s' % (self.svn_bakroot, os.sep, self.repo))
                finally:
                    if int(self.CurrentNum) >= int(self.StartNum):
                        DumpFile = '%s%s%s%s%s_%s_%s.dump' % (self.svn_bakroot, os.sep, self.repo, os.sep, self.repo, self.StartNum, self.CurrentNum)
                        try:
                            result = subprocess.check_call(r'svnadmin dump %s%s%s -r %s:head --incremental > %s' % (self.svn_reporoot, os.sep, self.repo, self.StartNum, DumpFile), shell=True)
                        except:
                            self.rv[self.repo]['result']='dump执行失败'
                            return rv
                        else:
                            if result == 0:
                                self.rv[self.repo]['CurrentNum'] = self.CurrentNum
                                self.rv[self.repo]['StartNum'] = self.StartNum
                                self.rv[self.repo]['DumpFile'] = DumpFile
                                self.rv[self.repo]['result'] = '备份成功'
                                return rv
                    else:
                        self.rv[self.repo]['result']='版本未增加'
                        return rv

            else:
                self.rv[self.repo]['result']='版本库为空'
                return rv

        else:
            self.rv[self.repo]['result'] = '版本库不存在'
            return rv


if __name__ == '__main__':
    rv={}
    for i in repos:
        new_thread=Svnbak(i,rv)
        new_thread.start()
