#coding:utf-8
from django.shortcuts import render_to_response

def base(request):
    return render_to_response('base.html')

def login(request):
    return render_to_response('login.html')