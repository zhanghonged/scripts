#coding:utf-8
import time
import paramiko
from django.shortcuts import render,redirect
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

def connect_server(ip,port,user,password):
    '''
    通过paramiko检测服务器是否可以连通，是的话返回连接对象
    :param ip:
    :param port:
    :param user:
    :param password:
    :return:返回连接对象
    '''
    result = {'status':'error','data':''}
    try:
        trans = paramiko.Transport(ip,port)
        trans.connect(username = user, password = password)
    except Exception as e:
        result['data'] = str(e)
    else:
        result['status'] = 'success'
        result['data'] = trans
    finally:
        return result

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
            connect = connect_server(ip,port,username,password)
            if connect['status'] == 'success':
                trans = connect['data']
                # 用于文件上传和下载的sftp服务
                sftp = paramiko.SFTPClient.from_transport(trans)
                # 远程执行命令服务
                ssh = paramiko.SSHClient()
                ssh._transport = trans
                # 创建目录
                stdin,stdout,stderr = ssh.exec_command('mkdir CMDBClient')
                time.sleep(1)
                # 上传文件
                sftp.put('sftpDir/getData.py','CMDBClient/getData.py')
                sftp.put('sftpDir/sendData.py', 'CMDBClient/sendData.py')
                sftp.put('sftpDir/main.py', 'CMDBClient/main.py')
                # 调用脚本
                stdin,stdout,stderr = ssh.exec_command('python CMDBClient/main.py')
                trans.close()
                # 连接成功状态记录到数据库
                equipment = Equipment.objects.get(ip=ip)
                equipment.status = 'True'
                equipment.save()
            else:
                result['data'] = connect['data']
                # 连接失败状态记录到数据库
                equipment = Equipment.objects.get(ip = ip)
                equipment.status = 'False'
                equipment.save()
        else:
            result['data'] = 'ip and port and username and password not be null'
    else:
        result['data'] = 'your request must be post'
    return JsonResponse(result)

# 由于客户端调用此接口，去掉csff验证
@csrf_exempt
def server_save(request):
    '''
    接收服务器发过来的系统信息，报错入库
    :param request:
    :return:
    '''
    result = {'status':'error','data':''}
    ip = request.META['REMOTE_ADDR']
    if request.method == 'POST':
        hostname = request.POST.get('get_hostname')
        sys_version = request.POST.get('get_systemVersion')
        mac = request.POST.get('get_mac')
        sys_type = request.POST.get('get_systeType')
        memory = request.POST.get('get_memory')
        cpu = request.POST.get('get_cpu')
        disk = request.POST.get('get_disk')

        try:
            equipment = Equipment.objects.get(ip=ip)
        except Exception ,e:
            print e
            result['data'] = str(e)
        else:
            equipment.hostname = hostname
            equipment.sys_version = sys_version
            equipment.mac = mac
            equipment.sys_type = sys_type
            equipment.memory = memory
            equipment.cpu = cpu
            equipment.disk = disk
            equipment.save()
            result["statue"] = "success"
            result["data"] = "your data is saved"
    else:
        result['data'] = 'request must be post'
    return JsonResponse(result)

def gateone(request):
    return render(request,'gateone.html')

def create_signature(secret,*parts):
    import hmac ,hashlib
    hash = hmac.new(secret, digestmod=hashlib.sha1)
    for part in parts:
        hash.update(str(part))
    return hash.hexdigest()

def get_auth_obj(request):
    gateone_server = 'http://192.168.1.5:8811'
    secret = 'secret'
    authobj = {
        'api_key':'YjQ3NjMyZjEyZTRjNDE5YzkwNWFlMGZiZDYwODI0YjUyY',
        'upn':'zhanghong',
        'timestamp':str(int(time.time() * 1000)),
        'signature_method':'HMAC-SHA1',
        'api_version':'1,0'
    }
    authobj['signature'] = create_signature(secret,authobj['api_key'],authobj['upn'],authobj['timestamp'])
    auth_info_and_server = {'url':gateone_server,'auth':authobj}
    return JsonResponse(auth_info_and_server)