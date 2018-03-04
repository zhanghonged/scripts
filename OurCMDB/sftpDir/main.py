#!/usr/bin/python
# coding:utf-8

import getData
from sendData import sendData

method_list = dir(getData)
method_dict = getData.__dict__  # 以字典形式，对象的方法名称作为键，属性本身作为值
result_dict = {}
for method in method_list:
    if method.startswith('get'):
        result_dict[method] = method_dict[method]

if __name__ == '__main__':
    print result_dict
    sendData(result_dict)
