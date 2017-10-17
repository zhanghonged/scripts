#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-09 14:49:12
# @Author  : zhanghong (zhanghonged@126.com)
# @Link    : http://blog.codecp.org/
# @Version : $Id$

import socket,os,sys,struct

host='192.168.1.123'
port=8811

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
s.listen(5)

while 1:
	conn,addr=s.accept()
	print 'Accept new connection from {0}'.format(addr)
	conn.send('Hi, Welcome to the server!')

	while 1:
		fileinfo_size=struct.calcsize('128sl')
		print 'fileinfo_size:',fileinfo_size
		buf=conn.recv(fileinfo_size)
		if buf:
			print 'buf:',buf
			filename,filesize = struct.unpack('128sl',buf)
			fn = filename.strip('\00')
			new_filename = os.path.join('./', 'new_' + fn)
			print 'file new name is {0}, filesize is {1}'.format(new_filename, filesize)

			recvd_size = 0
			fp = open(new_filename, 'wb')
			print 'start receiving...'

			while not recvd_size == filesize:
			    if filesize - recvd_size > 1024:
			        data = conn.recv(1024)
			        recvd_size += len(data)
			    else:
			        data = conn.recv(filesize - recvd_size)
			        recvd_size = filesize
			    fp.write(data)
			fp.close()
			print 'end receive...'
		conn.close()
		break