#coding:utf-8
import socket
import os
import struct

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(('localhost',10021))

while True:
    filename = raw_input('input filename:')
    if os.path.isfile(filename):
        fileinfo_size = struct.calcsize('128sl')
        fhead = struct.pack('128sl',os.path.basename(filename),os.path.getsize(filename))
        sock.send(fhead)

        fo = open(filename,'rb')
        while True:
            filedata = fo.read(1024)
            if not filedata:
                break
            sock.send(filedata)
        fo.close()
