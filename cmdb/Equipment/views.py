#coding:utf-8
import time
import paramiko
from django.shortcuts import render
from User.models import CMDBUser
from django.http import JsonResponse
from models import Equipment
from cmdb.views import getpage
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def server_list(request):
    '''
    服务器列表展示
    :param request:
    :return:
    '''
    uid = request.COOKIES.get('id')
    user = CMDBUser.objects.get(id = uid)
    return render(request,'serverlist.html',locals())

def server_list_data(request):
    '''
    :param request:
    :return:json类型返回服务器信息分页数据
    '''
    if request.method == 'GET':
        page = request.GET.get('page')
        num = request.GET.get('num')
        sql = 'select * from Equipment_equipment'
        if page and num:
            result = getpage(sql,page,num)
        elif page:
            result = getpage(sql,page)
        else:
            result = {
                'page_data': '',
                'page_range': '',
                'current_page': '',
                'max_page': ''
            }
    else:
        result = {
            'page_data': '',
            'page_range': '',
            'current_page': '',
            'max_page': ''
        }
    return JsonResponse(result)

def server_add(request):
    '''
    服务器添加方法，根据ip、port、username、password对服务器操作：远程登录、脚本上传、脚本远程执行
    :param request:
    :return:
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
                ssh._transport = trans
                #创建目录
                stdin,stdout,stderr = ssh.exec_command('mkdir CMDBClient')
                time.sleep(1)
                #上传文件
                sftp.put('sftpDir/getData.py','CMDBClient/getData.py')
                sftp.put('sftpDir/sendData.py', 'CMDBClient/sendData.py')
                sftp.put('sftpDir/main.py', 'CMDBClient/main.py')
                #调用脚本
                stdin,stdout,stderr = ssh.exec_command('python /root/CMDBClient/main.py')
                trans.close()
            except Exception as e:
                print e
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

# 由于客户端调用此接口，去掉csff验证
@csrf_exempt
def server_save(request):
    '''
    接收服务器发过来的系统信息，报错入库
    :param request:
    :return:
    '''
    ip = request.META['REMOTE_ADDR']
    if request.method == 'POST':
        hostname = request.POST.get('get_hostname')
        sys_version = request.POST.get('get_systemVersion')
        mac = request.POST.get('get_mac')
        sys_type = request.POST.get('get_systeType')
        memory = request.POST.get('get_memory')
        cpu = request.POST.get('get_cpu')


        print ip, type(ip)
        try:
            equipment = Equipment.objects.get(ip=ip)
        except Exception ,e:
            print e
        else:
            equipment.hostname = hostname
            equipment.sys_version = sys_version
            equipment.mac = mac
            equipment.sys_type = sys_type
            equipment.memory = memory
            equipment.cpu = cpu
            equipment.save()
    return JsonResponse({'data':'some'})


def host_connect(request):

    return render(request,'gateone.html',locals())

import hashlib,hmac
def get_auth_obj(request):
    # import time, hmac, hashlib, json
    user = request.user.username
    # 安装gateone的服务器以及端口.
    gateone_server = 'http://192.168.3.3'
    # 之前生成的api_key 和secret
    gateone_api_key = 'ZDcxMTRiNmZiN2NjNDQ4ODliN2YzMWEyMDBjZTE1NTc3M'
    gateone_secret = 'NzkyZDQxMmFjOTM3NGQzNjgwMmJkMTBlN2RjYjVhYzJhO'

    authobj = {
        'api_key': gateone_api_key,
        'upn': "gateone",
        'timestamp': str(int(time.time() * 1000)),
        'signature_method': 'HMAC-SHA1',
        'api_version': '1.0'
    }
    my_hash = hmac.new(gateone_secret, digestmod=hashlib.sha1)
    my_hash.update(authobj['api_key'] + authobj['upn'] + authobj['timestamp'])

    authobj['signature'] = my_hash.hexdigest()
    auth_info_and_server = {"url": gateone_server, "auth": authobj}
    # valid_json_auth_info = json.dumps(auth_info_and_server)
    # # logger.info(valid_json_auth_info)
    # return HttpResponse(valid_json_auth_info)
    return JsonResponse(auth_info_and_server)