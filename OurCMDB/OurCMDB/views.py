#coding:utf-8
import random
from django.shortcuts import render
from Admin.views import loginValid
from django.http import HttpResponseRedirect

@loginValid
def index(request):
    return render(request,'index.html')

content = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz'

def login(request):
    v_data = "".join(random.sample(content,28))
    response = render(request,'login.html',locals())
    response.set_cookie('key',v_data)
    return response

def logout(request):
    c_phone = request.COOKIES.get('phone')
    s_phone = request.session['phone']
    if c_phone and s_phone:
        del request.COOKIES['phone']
        # del request.session['phone']
        request.session.flush()
    return HttpResponseRedirect('/login')