#!/usr/bin/python
# -*- coding: utf-8 -*-
import zipfile, os, time, threading

"""
压缩并备份文件夹到指定目录
"""

__author__ = 'zhanghong'
__date__ = '2018/06/07'
__contact__ = 'zhanghonged@126.com'

sourceList = ["/opt/nginx/yiqunweb", "/opt/nginx/wechat","/usr/local/apache-tomcat-8.5.20/webapps/yiqun","/usr/local/office"]
backDir = "/opt/yimiaobackup"
thisDir = os.path.join(backDir, time.strftime('%Y%m%d_%H%M', time.localtime()))


def confirmBackDir():
    result = ""
    if not os.path.exists(backDir):
        print("%s 备份目录不存在，开始创建。" % backDir)
        try:
            os.mkdir(backDir)
        except Exception as e:
            print(str(e))
        else:
            print("备份目录 %s 创建成功。" % backDir)
    if not os.path.exists(thisDir):
        print("开始创建本次备份目录 %s." % thisDir)
        try:
            os.mkdir(thisDir)
        except Exception as e:
            print(str(e))
        else:
            print("本次备份目录 %s 创建成功。" % thisDir)
            result = thisDir
    else:
        print("本次备份目录 %s 已存在，请稍候再试。")
    return result


class YimiaoBackup(threading.Thread):
    def __init__(self,startDir,destDir):
        self.startDir = startDir
        self.destDir = destDir
        self.zip_file = self.startDir.rsplit(os.sep, 1)[-1] + '.zip'
        self.backup_file = os.path.join(self.destDir, self.zip_file)
        threading.Thread.__init__(self)

    def run(self):
        z = zipfile.ZipFile(self.backup_file, 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(self.startDir):
            # fpath = dirpath.replace(self.startDir, '')
            fpath = dirpath.replace(self.startDir, self.startDir.rsplit(os.sep,1)[-1])
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
                # print ('压缩文件 %s' % fpath + filename)
        z.close()
        print('%s--压缩完成--%s' % (self.startDir, self.backup_file))


if __name__ == "__main__":
    destDir = confirmBackDir()
    if destDir:
        for i in sourceList:
            new_thread = YimiaoBackup(i,destDir)
            new_thread.start()
