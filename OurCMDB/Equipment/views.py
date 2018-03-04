#coding:utf-8
import paramiko
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from models import *
from OurCMDB.views import getpage

# Create your views here.
def eq_list(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        num = request.GET.get('num')
        sql = 'select * from Equipment_equipment'
        if page and num:
            result = getpage(sql=sql, page=page,num=num)
        elif page:
            result = getpage(sql=sql,page=page)
        else:
            result = {
                'page_data': '',
                'page_range': ''
            }
    else:
        result = {
            'page_data': '',
            'page_range': ''
        }
    return JsonResponse(result)
def eq_list_page(request):
    eq_list = Equipment.objects.all()
    return render(request,'equipmentList.html',locals())

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



# import random
# def eq_add(request):
#     for i in range(100):
#         e = Equipment()
#         e.hostname = 'localhost_%s'%i
#         e.ip = '192.168.1.%s'%(i+2)
#         e.system = random.choice(['win7_32','win7_64','centos_6.5_x86','centos_6.5_x64','centos_7.4_x64','ubuntu','suse'])
#         e.status = random.choice(['True','False'])
#         e.mac = random.choice(['00:0c:29:92:f1:28','10:0c:29:92:f1:28','11:0c:29:92:f2:28','2b:0c:29:92:f1:28'])
#         e.username = random.choice(['root','admin','guset'])
#         e.password = '123'
#         e.port = 22
#         e.save()
#     return JsonResponse({'status':'true'})