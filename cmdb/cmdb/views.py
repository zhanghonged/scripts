#coding:utf-8
from django.shortcuts import render_to_response,render
from User.forms import Register
from User.models import CMDBUser
def valid_phone(phone):
    pass

def base(request):
    register = Register
    return render(request,'base.html',locals())

def login(request):
    return render_to_response('login.html')