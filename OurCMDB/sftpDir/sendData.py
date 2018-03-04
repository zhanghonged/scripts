#!/usr/bin/python
# coding:utf-8

import urllib, urllib2


def sendData(data):
    url = ''
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
    sendData = urllib.urlencode(data)  # urlencode 是用来将请求数据封装成为json格式
    request = urllib2.Request(url=url, headers=headers, data=sendData)
    response = urllib2.urlopen(request)
    content = response.read()