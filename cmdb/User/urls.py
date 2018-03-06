#coding:utf-8
from django.conf.urls import include, url
from views import *
urlpatterns = [
    url(r'^user_list/', user_list, name='user_list'),
    url(r'^userValid/', userValid, name='userValid'),
    url(r'^user_save', user_save, name='user_save'),
]