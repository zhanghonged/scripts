#coding:utf-8
import hashlib
from django.shortcuts import render, render_to_response
from django.http import JsonResponse, HttpResponseRedirect
from forms import Register, UserSetting
from models import CMDBUser
from cmdb.views import getpage ,loginValid
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@loginValid
def index(request):
    return render(request,'index.html')

def user_list(request):
    '''
    :param request:
    :return: 用户管理页
    '''
    register = Register
    return render(request,'userlist.html',locals())

def user_list_data(request):
    '''
    从数据库查询分页用户数据
    :param request:
    :return:json类型用户分页数据
    '''
    if request.method == 'GET':
        page = request.GET.get('page')
        num = request.GET.get('num')
        sql = 'select * from User_cmdbuser'
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
        obj = Register(request.POST)
        if obj.is_valid():
            print '表单校验成功:',obj.cleaned_data
            username = obj.cleaned_data['username']
            password = getmd5(obj.cleaned_data['password'])
            # 入库
            try:
                CMDBUser.objects.create(username=username,password=password)
            except Exception as e:
                print e
                result['data'] = '注册失败'
            else:
                result['status'] = 'success'
                result['data'] = '用户注册成功'

        else:
            print '表单校验失败:',obj.errors
            result['data'] = '注册失败'
    return JsonResponse(result)

def user_setting(request):
    '''
    用户个人设置
    :param request:
    :return:
    '''
    result = {'status':'error','data':''}
    if request.method == 'POST':
        phone = request.POST.get('phone'),
        #email = request.POST.get('email')
        uid = request.COOKIES.get('id')
        print uid
    return JsonResponse({'status':'aaa'})


def login(request):
    '''
    登录验证
    :param request:
    :return:
    '''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        loginvalid = request.POST.get('loginvalid')
        token_cookie = request.COOKIES.get('token')

        # 判断前端页面的值与token_cookie的值是否相同，这是一种反爬手段
        if loginvalid == token_cookie:
            try:
                user = CMDBUser.objects.get(username=username)
            except:
                return HttpResponseRedirect('/login/')
            else:
                if user.password == getmd5(password):
                    response = HttpResponseRedirect('/')
                    response.set_cookie('id',user.id)
                    request.session['isLogin'] = True
                    return response
                else:
                    return HttpResponseRedirect('/login/')
        else:
            return HttpResponseRedirect('/login/')
    return HttpResponseRedirect('/login/')
