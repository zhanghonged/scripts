#coding:utf-8
import hashlib
from django.shortcuts import render
from forms import Register
from models import User
from django.http import JsonResponse, HttpResponseRedirect
# Create your views here.

def userValid(request):
    '''
    验证用户名是否已存在
    '''
    result = {'valid':False}
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            try:
                u = User.objects.get(username = username)
            except:
                result['valid'] = True
    return JsonResponse(result)

def phoneValid(request):
    '''
    验证手机号是否已存在
    '''
    result = {'valid':False}
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if phone:
            try:
                u = User.objects.get(phone = phone)
            except:
                result['valid'] = True
    return JsonResponse(result)

def emailValid(request):
    '''
    验证邮箱是否已存在
    '''
    result = {'valid': False}
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                u = User.objects.get(email = email)
            except:
                result['valid'] = True
    return JsonResponse(result)

def loginValid(fun):
    '''
    验证用户登录状态
    '''
    def inner(request, *args, **kwargs):
        c_phone = request.COOKIES.get('phone')
        s_phone = request.session.get('phone')
        if c_phone and c_phone == s_phone:
            return fun(request,*args, **kwargs)
        else:
            return HttpResponseRedirect('/login')
    return inner

def login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        valid_remember = request.POST.get('valide')
        cookie_remember = request.COOKIES.get('key')
        if valid_remember == cookie_remember:
            try:
                u = User.objects.get(phone = phone)
            except:
                return HttpResponseRedirect('/login')
            else:
                post_password = getmd5(password)
                if post_password == u.password:
                    response = HttpResponseRedirect('/index')
                    response.set_cookie('phone', u.phone)
                    request.session['phone'] = u.phone
                    return response
                else:
                    return HttpResponseRedirect('/login')
        else:
            return HttpResponseRedirect('/login')
    return HttpResponseRedirect('/login')

def logout(request):
    pass

def register(request):
    pass

def getmd5(password):
    '''
    密码加密
    '''
    md5 = hashlib.md5()
    md5.update(password)
    return md5.hexdigest()

def user_list(request):
    '''
    用户注册
    '''
    register = Register
    if request.method == 'POST':
        obj = Register(request.POST,request.FILES)
        if obj.is_valid():
            print '表单校验成功:',obj.cleaned_data
            user_data = obj.cleaned_data
            user_data['password'] = getmd5(user_data['password'])
            print user_data['password']
            User.objects.create(**user_data)
        else:
            print '校验失败:',obj.errors
    return render(request,'userList.html',locals())

def user_alter(request):
    pass

def user_drop(request):
    pass