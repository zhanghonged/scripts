#coding:utf-8
from django.conf.urls import include, url
from views import *
urlpatterns = [
    url(r'^$',eq_list_page,name='eq_list_page'),
    url(r'^eq_save/',eq_save,name='eq_save'),
    url(r'^eq_connect',eq_connect,name='eq_connect'),
    url(r'eq_list',eq_list,name='eq_list')
]
