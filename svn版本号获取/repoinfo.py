#!/usr/bin/python
#coding:utf-8

import os
import re
import sys


"""
版本发布信息生成
自动生成svn版本库最新版本号
"""

__author__ = 'zhanghong'
__date__ = '2018/06/08'
__contact__ = 'zhanghonged@126.com'

repos = {
    '前台':'http://192.168.1.5/svn/Project/yiqun/src/trunk/yiqunweb/yiqunweb',
    '微信':'http://192.168.1.5/svn/Project/yiqun/src/trunk/wechat',
    '后台':'http://192.168.1.5/svn/Project/yiqun/src/trunk/yiqun',
    'office':'http://192.168.1.5/svn/Project/yiqun/src/trunk/office',
    'jacob':'http://192.168.1.5/svn/Project/yiqun/src/trunk/jacob'
}

def getInfo(url):
    t = os.popen('svn info %s' %url)
    var = t.read()

    list = var.splitlines()
    for str in list:
        #print(str)
        if str.startswith('最后修改的版本:'):
            version = re.findall("\d+",str)
            return version[0]



if __name__ == "__main__":
    result = []
    for key,value in repos.items():
        result.append('%s_%s' %(key,getInfo(value)))
    repoInfo = ' '.join(result)
    try:
        version = sys.argv[1]
    except:
        version = ' '
    finally:
        print('译喵v%s %s' %(version,repoInfo))
