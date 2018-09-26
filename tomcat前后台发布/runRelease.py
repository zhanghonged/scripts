#!/usr/bin/python
#coding:utf-8
import os
import sys
import time
import datetime
import hashlib
import shutil
import telnetlib
import glob

__author__ = 'zhanghong'
__date__ = '2018/09/26'
__contact__ = 'zhanghonged@126.com'


tomcatDir = "/usr/local/apache-tomcat-8.5.20"
tomcatHost='127.0.0.1'
tomcatPort=8088

def clearlog():
    """
    处理tomcat日志
    out结尾的log重命名备份，其他清除
    """
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    #logfile = "catalina.out.%s.out"%today
    #cmd = "cat /dev/null > %s" %os.path.join(tomcatDir,"logs",logfile)
    #os.system(cmd)
    
    logfile = os.path.join(tomcatDir,"logs","catalina.out.%s.out"%today)
    if os.path.isfile(logfile):
        os.rename(logfile, logfile+'-bak')
    map(os.remove, glob.glob(tomcatDir + "/logs/*.log"))
    map(os.remove, glob.glob(tomcatDir + "/logs/*.txt"))
    #map(os.remove, glob.glob(tomcatDir + "/logs/*.out"))

def stop_tomcat():
    """
    关闭tomcat服务
    """
    clearlog()
    print("tomcat正在关闭，请稍候...")
    os.system("ps aux | grep tomcat | grep -v grep | awk '{print $2}'|xargs kill -9")
    time.sleep(2)
    try:
        tel = telnetlib.Telnet(tomcatHost,tomcatPort)
    except:
        print("tomcat关闭成功")
    else:
        print("tomcat关闭失败，请手动检查")

def start_tomcat():
    """
    启动tomcat 
    """
    clearlog()
    print("tomcat正在启动，请稍候...")
    cmd = os.path.join(tomcatDir,'bin/startup.sh')
    os.system(cmd)
    time.sleep(3)
    for k in range(60,0,-1):
        print(k)
        time.sleep(1)
        os.system("clear")
   
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    logfile = os.path.join(tomcatDir,"logs","catalina.%s.log"%today)
    with open (logfile,"r") as f:
        try:
            tel =  telnetlib.Telnet(tomcatHost,tomcatPort)
        except:
            print("tomcat启动失败，请手动检查!!!")
        else:
            log = f.read()
            log.index("Server startup in")
            print("tomcat即将启动完成，请继续等待3秒。")
            time.sleep(4)
            print("tomcat启动成功")




def getFileMd5(filename):
    """
    计算文件的MD5
    """
    myhash = hashlib.md5()
    with open(filename,"r") as f:
        while True:
            b = f.read(8096)
            if not b:
                break
            myhash.update(b)
    return myhash.hexdigest()

def copyFiles(sourceDir,targetDir):
    """
    复制目录下所有文件到指定目录
    """
    for file in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir,file)
        targetFile = os.path.join(targetDir,file)
        if os.path.isfile(sourceFile):
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            if not os.path.exists(targetFile) or (os.path.exists(targetFile) and (getFileMd5(sourceFile) != getFileMd5(targetFile))):
                open(targetFile, "wb").write(open(sourceFile, "rb").read())
                print('复制文件%s 到---> %s'%(sourceFile,targetFile))
        if os.path.isdir(sourceFile):
            First_Directory = False
            copyFiles(sourceFile,targetFile)


def frontDeploy(updateSourceDir,frontFilename,frontTargetDir):
    """
    前端静态文件发布
    """
    updateSourceZipFile = os.path.join(updateSourceDir,frontFilename)
    updateSourceFile = updateSourceZipFile.split(".")[0]
    if os.path.isfile(updateSourceZipFile):
        # 如果已存在解压后的文件，先删除再解压    
        if os.path.exists(updateSourceFile):
            shutil.rmtree(updateSourceFile)
        print("开始解压缩文件%s..."%updateSourceZipFile)
        os.popen("/usr/bin/unzip -d %s %s"%(updateSourceDir, updateSourceZipFile))
        print("解压缩完成")
        # 开始拷贝文件到目标路径
       
        copyFiles(updateSourceFile,frontTargetDir)
    else:
        print("更新文件不存在,前端web更新失败！")
        sys.exit()
    

def backgroundDeploy(updateSourceDir ,backgroundJar, backgroundWar, deployment="war"):
    """
    部署tomcat后台服务
    分为jar包局部更新和war包整包更新
    """
    if deployment == "jar":
        print("开始进行后台jar包局部更新...")
        updateSourceJar = os.path.join(updateSourceDir,backgroundJar)
        if os.path.isfile(updateSourceJar):
            stop_tomcat()
            time.sleep(1)
            cmd = "cd %s/webapps/yiqun/WEB-INF/classes && jar xvf %s" %(tomcatDir,updateSourceJar)
            os.system(cmd)
            print("后台jar包部署完成，稍候开始启动tomcat...")
            time.sleep(1)
            start_tomcat()
        else:
            print("更新文件%s 不存在，后台更新失败!"%updateSourceJar)
        
    elif deployment == "war":
        print("开始进行后台war包整包更新...")
        updateSourceWar = os.path.join(updateSourceDir,backgroundWar)
        if os.path.isfile(updateSourceWar):
            stop_tomcat()
            time.sleep(1)
            oldAppWar = os.path.join(tomcatDir, "webapps", backgroundWar)
            oldApp = oldAppWar.rsplit('.',1)[0]
            print("oldAppWar:"+oldAppWar)
            print("oldApp:"+oldApp)
            # 删除webapps下老的war包
            if os.path.isfile(oldAppWar):
                os.remove(oldAppWar)
            # 删除webapps下解压后的老的app目录
            if os.path.exists(oldApp):
                shutil.rmtree(oldApp)
            # 拷贝新的war包到webapps下
            shutil.copy(updateSourceWar,os.path.join(tomcatDir,'webapps'))
            print("后台war包部署完成，稍候开始启动tomcat...")
            time.sleep(1)
            start_tomcat()
        else:
            print("更新文件%s 不存在，后台更新失败!"%updateSourceJar)



if __name__ == "__main__":
    day = datetime.datetime.now().strftime('%Y%m%d')
    updateSourceDir = os.path.join("/root/fabu",day)
    frontFilename = "yiqunweb.zip"
    frontTargetDir = "/opt/nginx/yiqunweb"
    backgroundJar = "yiapi.jar"
    backgroundWar = "yiqun.war"

    action = raw_input("更新前请确认是否完成备份Y/N:")
    
    if action in ("Y","y"):
        if len(sys.argv) < 2 or sys.argv[1] not in ("front","background-jar","background-war"):
            print("Usage %s {front | background-jar | background-war}"%sys.argv[0])
        elif sys.argv[1] == "front":
            print("前台更新")
            frontDeploy(updateSourceDir,frontFilename,frontTargetDir)
        elif sys.argv[1] == "background-jar":
            print("后台更新jar")
            backgroundDeploy(updateSourceDir,backgroundJar,backgroundWar,"jar")
        elif sys.argv[1] == "background-war":
            print("后台更新war")
            backgroundDeploy(updateSourceDir,backgroundJar,backgroundWar,"war")
    else:
        sys.exit()
