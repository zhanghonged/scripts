#coding:utf-8
import hashlib
from django.shortcuts import render, render_to_response
from django.http import JsonResponse
from forms import Register
from models import CMDBUser
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render_to_response('index.html')


def user_list(request):
    register = Register
    return render(request,'userlist.html',locals())

def userValid(request):
    '''
    验证用户名是否已经注册
    :param request:
    :return:返回json对象
    '''
    result = {'valid':False}
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            try:
                u = CMDBUser.objects.get(username=username)
            except:
                result['valid'] = True
    return JsonResponse(result)

def getmd5(password):
    '''
    密码加密
    :param password: 用户输入的密码
    :return: 加密后的字符串
    '''
    md5 = hashlib.md5()
    md5.update(password)
    return md5.hexdigest()

def user_save(request):
    '''
    注册用户
    :param request:
    :return:
    '''
    result = {'status':'error','data':''}
    if request.method == 'POST':
        register = Register
        obj = Register(request.POST,request.FILES)
        if obj.is_valid():
            print '表单校验成功:',obj.cleaned_data
            username = obj.cleaned_data['username']
            password = getmd5(obj.cleaned_data['password'])
            photo = obj.cleaned_data['photo']
            # 入库
            try:
                CMDBUser.objects.create(username=username,password=password,photo=photo)
            except Exception as e:
                print e
                result['data'] = '注册失败'
            else:
                result['status'] = 'success'
                result['data'] = '用户注册成功'

        else:
            print '表单校验失败:',obj.errors
            result['data'] = '注册失败'
    print result
    return JsonResponse(result)