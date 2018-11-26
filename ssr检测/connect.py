#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time
import commands
import random
import threading
from genSSR import getConfig

class TestSsr(threading.Thread):

  def __init__(self,s,logfile):
    self.timeout = "10"
    self.test_url = "https://google.com"
    self.ssr_folder= "/root/shadowsocksr/shadowsocks"
    self.localport = random.randint(1900,1999)
    self.logfile = logfile

    config = getConfig(s)
    self.ip = config["ip"]
    self.port = config["port"]
    self.passwd = config["passwd"]
    self.method = config["method"]
    self.protocol = config["protocol"]
    self.obfs = config["obfs"]
    threading.Thread.__init__(self)


  def run(self):

    # 启动 ShadowsocksR客户端进程
    cmd = "nohup python %s/local.py -b '127.0.0.1' -l %s -s %s -p %s -k %s -m %s -O %s -o %s > /dev/num 2>&1 &"%(self.ssr_folder,self.localport,self.ip,self.port,self.passwd,self.method,self.protocol,self.obfs)
    os.system(cmd)
    time.sleep(2)

    # 查出当前ShadowsocksR的进程号
    pid_cmd = "ps -ef | grep 'local.py -b 127.0.0.1 -l %s' | grep -v grep | awk '{print $2}'"%self.localport
    pid_status,pid_output = commands.getstatusoutput(pid_cmd)
    if pid_status ==0 and pid_output.strip() != "":
      PID = pid_output

      # 开始进行检测
      test_cmd = "curl --socks5 127.0.0.1:%s -k -m %s -s %s"%(self.localport,self.timeout,self.test_url)
      test_status,test_output = commands.getstatusoutput(test_cmd)
      if test_status == 0 and test_output.strip() != "":
        print "[%s:%s] 检测成功，账号可用！"%(self.ip,self.port)
        with open(self.logfile,'ab+') as f:
          f.write("[%s:%s] 检测成功，账号可用！\n"%(self.ip,self.port))
      else:
        print "[%s:%s] 检测失败，账号异常，不可用!"%(self.ip,self.port)
        with open(self.logfile,'ab+') as f:
          f.write("[%s:%s] 检测失败，账号异常，不可用!\n"%(self.ip,self.port))

      # 检测完成kill掉 ShadownsocksR客户端进程
      kill_status,kill_output = commands.getstatusoutput("kill -9 %s"%PID)
      if kill_status != 0:
        print "error! ShadowsocksR客户端 停止失败，请检查 !"
    else:
      print "ShadowsocksR客户端进程启动失败，请查看！"


if __name__ == "__main__":
  config_file = "./ssr_check.conf"
  if os.path.isfile(config_file):
    try:
      with open(config_file,"r") as f:
        configs = f.readlines()
    except Exception as e:
        print("config_file文件打开失败:%s")%str(e)
    else:

      logfile = "%s.log"%time.strftime('%Y%m%d-%H%M%S',time.localtime())
      with open (logfile,'wb') as f:
        f.write("=====开始记录测试信息 %s=====\n"%time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))

      threads = []
      for config in configs:
        if config.strip() != "":
          new_thread = TestSsr(config.strip(),logfile)
          threads.append(new_thread)
          new_thread.start()

      # 等待所有线程结束后，写入结束时间
      for t in threads:
        t.join() 
      
      with open (logfile,'ab+') as f:
        f.write("=====测试结束 %s=====\n"%time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
  else:
    print "config_file文件不存在，检测失败!"
