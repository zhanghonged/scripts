#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-09 16:28:09
# @Author  : zhanghong (zhanghonged@126.com)
# @Link    : http://blog.codecp.org/
# @Version : $Id$

import socket,os,sys,struct

host='192.168.1.123'
port=8811

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))


while 1:
	filepath=raw_input('Please input file path: ')
	if os.path.isfile(filepath):
		fileinfo_size=struct.calcsize('@128sl')
		print 'fileinfo_size',fileinfo_size
		print 'filename',os.path.basename(filepath)
		print 'filesize',os.stat(filepath).st_size
		fhead=struct.pack('@128sl',os.path.basename(filepath),os.stat(filepath).st_size)
		s.send(fhead)

		print 'client filepath: {0}'.format(filepath)

		fp=open(filepath,'rb')
		while 1:
			data=fp.read(1024)
			if not data:
				print '{0} file send over...'.format(filepath)
				break
			s.send(data)
	s.close()
	break