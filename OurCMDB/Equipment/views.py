#coding:utf-8
import paramiko
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from models import *

# Create your views here.
def eq_list(request):
    return render(request,'equipmentList.html')

def eq_connect(request):
    '''
    connect 方法实现 远程登录、脚本上传、脚本远程执行
    '''
    result = {'status':'error','data':''}
    if request.method == 'POST':
        ip = request.POST.get('ip')
        port = request.POST.get('port')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print ip,port,username,password
        if ip and port and username and password:
            #save db
            equipment = Equipment()
            equipment.ip = ip
            equipment.port = port
            equipment.username = username
            equipment.password = password
            equipment.save()
            #连接远程虚拟机
            try:
                trans = paramiko.Transport(ip,port)
                trans.connect(username=username,password=password)

                sftp = paramiko.SFTPClient.from_transport(trans) #用于文件上传和下载的sftp服务
                ssh = paramiko.SSHClient() #远程执行命令的服务
                ssh.get_transport = trans
                #创建目录
                stdin,stdout,stderr = ssh.exec_command('mkdir CMDBClient')
                #上传文件
                sftp.put('sftpDir/getData.py','CMDBClient/getData.py')
                sftp.put('sftpDir/sendData.py', 'CMDBClient/sendData.py')
                sftp.put('sftpDir/main.py', 'CMDBClient/main.py')
                #调用脚本
                stdin,stdout,stderr = ssh.exec_command('python /root/CMDBClient/main.py')
                trans.close()
            except:
                equipment = Equipment.objects.get(ip = ip)
                equipment.status = 'False'
                result['data'] = '连接服务器失败'
            else:
                equipment = Equipment.objects.get(ip = ip)
                equipment.status = 'True'
                result['status'] = 'success'
                result['data'] = '添加成功'
            finally:
                equipment.save()
        else:
            result['data'] = '添加失败'
    else:
        result['data'] = '添加失败'
    return JsonResponse(result)

def eq_add(request):
    pass

def eq_drop(request):
    pass

def eq_alter(request):
    pass

@csrf_exempt
def eq_save(request):
    ip = request.META['REMOTE_ADDR']
    if request.method == 'POST':
        hostname = request.POST.get('get_hostname')
        system = request.POST.get('get_system')
        mac = request.POST.get('get_mac')

        equipment = Equipment.objects.get(ip = ip)
        equipment.hostname = hostname
        equipment.system = system
        equipment.mac = mac
        equipment.save()
    return JsonResponse({'state':'this only a test'})