#!/usr/bin/python
#coding:utf-8

import os
import socket
import sys
from supervisor import childutils
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import Encoders

class CrashMail:

  def __init__(self):

    self.mail_from = '233571510@qq.com'
    self.mail_passwd = 'xxxxxxxxxx'
    self.mail_smtp = 'smtp.qq.com'
    self.mail_smtp_port = 465
    self.mail_to = ['zhanghong@16feng.com']

    self.stdin = sys.stdin
    self.stdout = sys.stdout
    self.stderr = sys.stderr

  def runforever(self, test=False):
    # 定义一个无限循环，可以循环处理event
    # 当然也可以不用循环，把listener的autorestart 配置为 true，处理完一次event就让该listener退出，然后supervisord重启该listener，这样listen#er就可以处理新的event了
    while 1:
      # 从这里开始，是向stdout发送"READY"，然后就阻塞在这里，一直等到有event发过来再开始处理


      # 收到消息后
      # headers, payload 分别是接收到的header和body的内容
      headers, payload = childutils.listener.wait(self.stdin, self.stdout)

      if test:
        self.stderr.write(str(headers) + '\n')
        self.stderr.write(payload + '\n')
        self.stderr.flush()

      # 判断 event类型 是否是咱们需要的，不是的话，向stdout写入"RESULT\nOK"，并跳过当前循环的剩余部分
      if not headers['eventname'] == 'PROCESS_STATE_EXITED':
        childutils.listener.ok(self.stdout)
        continue

      # 解析 payload, 这里我们只用这个 pheaders
      # pdata 在 PROCESS_LOG_STDERR 和 PROCESS_COMMUNICATION_STDOUT 等类型的 event 中才有
      pheaders, pdata = childutils.eventdata(payload+'\n')

      # 过滤掉 expected 的 event, 仅处理 unexpected 的
      # 当 program 的退出码为对应配置中的 exitcodes 值时, expected=1; 否则为0
      if int(pheaders['expected']):
        childutils.listener.ok(self.stdout)
        continue

      hostname = socket.gethostname()
      ip = socket.gethostbyname(hostname)

      # 构造报警内容
      message = "Host: %s(%s)\nProcess: %s\nPID: %s\nEXITED unexpectedly from state: %s" % \
            (hostname, ip, pheaders['processname'], pheaders['pid'], pheaders['from_state'])

      # 构建报警标题
      subject = ' %s crashed at %s' % (pheaders['processname'], childutils.get_asctime())

      # 输出mail信息
      self.stderr.write('unexpected exit, mailing\n')
      self.stderr.flush()

      # 触发邮件报警
      self.mail(subject, message)

      # 向 stdout 写入"RESULT\nOK"，并进入下一次循环
      childutils.listener.ok(self.stdout)


  def mail(self, subject, message):

    msg = MIMEMultipart()
    mail_body = MIMEText(message,'plain','utf-8')
    msg.attach(mail_body)
    msg['Subject'] = subject    
    msg['from'] = self.mail_from
    msg['to'] = ','.join(self.mail_to)
    try:
      server = smtplib.SMTP_SSL(self.mail_smtp, self.mail_smtp_port)
      server.login(self.mail_from,self.mail_passwd)
      server.sendmail(self.mail_from,self.mail_to,msg.as_string())
      server.quit()
    except smtplib.SMTPException as e:
      print(str(e))
      print('邮件发送失败')

    

def main(argv=sys.argv):


  if not 'SUPERVISOR_SERVER_URL' in os.environ:
    sys.stderr.write('crashmail must be run as a supervisor event listener\n')
    sys.stderr.flush()
    return

  prog = CrashMail()
  prog.runforever(test=True)

if __name__ == "__main__":
  main()
