#coding:utf-8
from django.conf.urls import include, url
from views import *

urlpatterns = [
    url(r'^server_list/', server_list, name='server_list'),
    url(r'^server_list_data', server_list_data, name='server_list_data'),
    url(r'^server_add', server_add, name='server_add'),
    url(r'^server_save', server_save, name='server_save'),
    url(r'^shell/', shell, name='shell'),
    url(r'cmd', command, name='cmd'),
]