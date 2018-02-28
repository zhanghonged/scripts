#coding:utf-8
from django.conf.urls import include, url
from django.contrib import admin
from views import *
urlpatterns = [
    url(r'^$', user_list, name='user_list'),
    url(r'^userValid/$', userValid, name='userValid'),
    url(r'^phoneValid/$', phoneValid, name='phoneValid'),
    url(r'^emailValid/$', emailValid, name='emailValid'),
    url(r'login/$',login, name='login'),
]