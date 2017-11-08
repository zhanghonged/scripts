#coding:utf-8

import os,commands

#装饰器，用于记录备份完成后的版本号
def decorator(svn_reporoot='/opt/svndata'):
    def revision(fun):
        def wrapper(repo):
            if fun(repo) == '备份成功':
                RecordVersion = '%s_LastRevision.txt' % repo
                CurrentNum = os.popen('svnlook youngest %s/%s' % (svn_reporoot, repo)).read().strip()
                with open(RecordVersion,'wb') as f:
                    f.write(CurrentNum)
            else:
                print '备份出错，不记录'
        return wrapper
    return revision


@decorator()
def repobak(repo,svn_reporoot='/opt/svndata'):

    RecordVersion='%s_LastRevision.txt'%repo
    #查看版本库当前的版本号
    CurrentNum=os.popen('svnlook youngest %s/%s'%(svn_reporoot,repo)).read().strip()
    if CurrentNum > 0:
        #从文件中获取上次备份完成后记录的版本号
        try:
            with open(RecordVersion,'rb') as f:
                StartNum=int(f.read())+1
        except:
            StartNum=0
        finally:
            if CurrentNum > StartNum:
                #开始备份
                DumpFile='%s_%s_%s.dump'%(repo,StartNum,CurrentNum)
                result=commands.getstatusoutput('svnadmin dump %s/%s -r %s:head --incremental > %s'%(svn_reporoot,repo,StartNum,DumpFile))
                if result[0] == 0:
                    return '备份成功'
                else:
                    return '备份出错'

repobak('fx')