#coding:utf-8

import os
import datetime
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

##发件相关设置
mail_from = '233571510@qq.com'
mail_passwd='gbiukcxoumkwbgca'
mail_smtp='smtp.qq.com'
mail_smtp_port=465
mail_to = ['zhanghong@16feng.com','shemq@16feng.com']

##需要备份的版本库
repos=['fx','Abc','test']

#装饰器作用：1、记录备份后的版本号。2、备份后写log。3、备份后发送邮件提醒。
def decorator(svn_reporoot,svn_bakroot):
    def revision(fun):
        def wrapper(repo):
            result=fun(repo)
            RecordVersion_file = '%s%s%s%s%s_LastRevision.txt' % (svn_bakroot, os.sep, repo, os.sep, repo)
            Log_file = '%s%s%s%s%s_log.txt' % (svn_bakroot, os.sep, repo, os.sep, repo)
            if result['result'] == '备份成功':
                print '备份成功，记录这次备份的版本号%s' % result['CurrentNum']
                with open(RecordVersion_file,'wb') as f:
                    f.write(result['CurrentNum'])
                print '开始记录log'
                with open(Log_file,'ab+')as f:
                    f.write(str(datetime.datetime.now()))
                    f.write('  -- 添加备份文件 %s，从[%s]到[%s]。'%(result['DumpFile'],result['StartNum'],result['CurrentNum'])+'\n')

                title='svn版本库%s备份成功%s_%s'%(repo,result['StartNum'],result['CurrentNum'])
                mail_body='Svn版本库%s备份成功：\n版本库：%s\n备份时间：%s\n版本号：[%s]_[%s]'%(repo,repo,datetime.datetime.now(),result['StartNum'],result['CurrentNum'])
            elif result['result'] == '版本库不存在':
                print '%s版本库不存在,无需备份!'%repo
                title = 'svn版本库%s备份未进行' %repo
                mail_body = 'Svn版本库%s备份未进行：\n版本库：%s\n时间：%s\n未进行原因：%s' % (repo,repo,datetime.datetime.now(),result['result'])
            elif result['result'] == '版本库为空':
                print '%s版本库为空,无需备份!'%repo
                title = 'svn版本库%s备份未进行' %repo
                mail_body = 'Svn版本库%s备份未进行：\n版本库：%s\n时间：%s\n未进行原因：%s' % (repo,repo,datetime.datetime.now(),result['result'])
            elif result['result'] == '版本未增加':
                print '%s版本未增加,无需备份!'%repo
                title = 'svn版本库%s备份未进行' %repo
                mail_body = 'Svn版本库%s备份未进行：\n版本库：%s\n时间：%s\n未进行原因：%s' % (repo,repo,datetime.datetime.now(),result['result'])
            else:
                print '%s版本库备份失败!'
                title = 'svn版本库%s备份失败' % (repo)
                mail_body = 'Svn版本库%s备份失败：\n版本库：%s\n时间：%s\n版本号：[%s]_[%s]\n失败原因：%s' % (repo,repo,datetime.datetime.now(),result['StartNum'],result['CurrentNum'],result['result'])

            msg=MIMEMultipart()
            body=MIMEText(mail_body,'plain','utf-8')
            msg.attach(body)
            msg['Subject']=title
            msg['from']=mail_from
            msg['to']=','.join(mail_to)
            try:
                server=smtplib.SMTP_SSL(mail_smtp,mail_smtp_port)
                server.login(mail_from,mail_passwd)
                server.sendmail(mail_from,mail_to,msg.as_string())
                server.quit()
                print '邮件发送成功'
            except smtplib.SMTPException as e:
                print e
                print '邮件发送失败'
        return wrapper
    return revision


@decorator(r'E:\Repositories',r'E:\bak')
def repobak(repo,svn_reporoot=r'E:\Repositories',svn_bakroot=r'E:\bak'):
    rv={}
    RecordVersion_file='%s%s%s%s%s_LastRevision.txt' %(svn_bakroot,os.sep,repo,os.sep,repo)
    #查看版本库当前的版本号
    CurrentNum=os.popen('svnlook youngest %s/%s'%(svn_reporoot,repo)).read().strip()
    if CurrentNum:
        if int(CurrentNum) > 0:
            #从文件中获取上次备份完成后记录的版本号
            try:
                with open(RecordVersion_file,'rb') as f:
                    StartNum=int(f.read())+1
            except:
                StartNum=0
                #第一次备份时创建备份目录
                if not os.path.isdir('%s%s%s'%(svn_bakroot,os.sep,repo)):
                    os.makedirs('%s%s%s'%(svn_bakroot,os.sep,repo))
            finally:
                if int(CurrentNum) >= int(StartNum):
                    #开始备份
                    DumpFile='%s%s%s%s%s_%s_%s.dump'%(svn_bakroot,os.sep,repo,os.sep,repo,StartNum,CurrentNum)
                    try:
                        result=subprocess.check_call(r'svnadmin dump %s%s%s -r %s:head --incremental > %s'%(svn_reporoot,os.sep,repo,StartNum,DumpFile),shell=True)
                    except:
                        rv['result']='dump执行失败'
                        return rv
                    else:
                        if result == 0:
                            rv['CurrentNum'] = CurrentNum
                            rv['StartNum'] = StartNum
                            rv['DumpFile'] = DumpFile
                            rv['result']='备份成功'
                            return rv
                else:
                    rv['result']='版本未增加'
                    return rv
        else:
            rv['result']='版本库为空'
            return rv
    else:
        rv['result']='版本库不存在'
        return rv

if __name__ == '__main__':
    for i in repos:
        repobak(i)