#coding:utf-8
from django.shortcuts import render
from forms import Register
from models import User
from django.http import JsonResponse
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

def loginValid(request,*args,**kwargs):
    pass

def login(request):
    pass

def logout(request):
    pass

def register(request):
    pass

def user_list(request):
    register = Register
    if request.method == 'POST':
        obj = Register(request.POST,request.FILES)
        if obj.is_valid():
            print '表单校验成功:',obj.cleaned_data
            photo = obj.cleaned_data['photo']
            print photo
            print type(photo)
            User.objects.create(**obj.cleaned_data)
        else:
            print '校验失败:',obj.errors
    return render(request,'userList.html',locals())

def user_alter(request):
    pass

def user_drop(request):
    pass