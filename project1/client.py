#coding:utf-8

import os
import time
import socket
import hashlib
from model import User



class Userdo(object):
    def __init__(self):
        pass

    def encry(self,password):
        serc=hashlib.md5('加密')
        serc.update(password)
        return serc.hexdigest()

    def register(self):
        self.username = raw_input('Enter username:')
        try:
            user = User.get(User.username == self.username)
        except:
            user = User()
            self.password = raw_input('Enter password:')
            if self.password.isalnum() and len(self.password) >= 6:
                self.password2 = raw_input('Enter password again:')
                if self.password == self.password2:
                    user.username = self.username
                    user.password = self.encry(self.password)
                    user.register_time = time.strftime('%Y-%m-%d %H:%M:%S')
                    user.save()
                    print 'sign successfully.'
                    return True
                else:
                    print 'The two passwords don\'t same!'
            else:
                print 'Must include Numbers and letters, and length is greater than 6!'
        else:
            print 'username already exists!'

    def login(self):
        self.username = raw_input('username:')
        try:
            user = User.get(User.username == self.username)
        except:
            print 'username does not exist!'
        else:
            self.password = self.encry(raw_input("password:"))
            for i in range(2):
                if self.password == user.password:
                    print 'login Success.'
                    return self.username
                else:
                    self.password = self.encry(raw_input('password error, please re-enter:'))
                    if self.password == user.password:
                        print 'login Success.'
                        return self.username
            else:
                print 'More than three times. Please Just a moment.'

class Socketclient(object):
    def __init__(self,host,port,user):
        self.host = host
        self.port = port
        self.user = user
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((self.host,self.port))

    def sendhead(self,head):
        self.sock.send(head)
        rdata = self.sock.recv(512)
        return rdata

    def sendfile(self):
        with open(self.file_path, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                self.sock.send(data)

    def recvfile(self):
        recev_size = 0
        with open(self.file_name, 'wb') as f:
            self.sock.send('begin')
            print 'start recv %s..........' % self.file_name
            while not recev_size == self.file_size:
                if self.file_size - recev_size > 1024:
                    rdata = self.sock.recv(1024)
                    recev_size += len(rdata)
                else:
                    rdata = self.sock.recv(self.file_size - recev_size)
                    recev_size = self.file_size
                f.write(rdata)
        print 'receive %s done...' % self.file_name

    def start(self):
        while True:
            command = raw_input("'put file' or 'get file' or 'quit':")
            if command == 'quit':
                return
            if not command:
                continue
            else:
                self.file_action, self.file_path = command.split()
                # 将file_path解码为unicode
                self.file_path = self.file_path.decode('utf-8')
                if self.file_action == 'put':
                    if os.path.isfile(self.file_path):
                        self.file_name = os.path.basename(self.file_path)
                        self.file_size = os.path.getsize(self.file_path)
                        # 由于socket不能传送unicode编码,因此编码成utf-8,使变成str格式
                        self.fhead = ' '.join([self.file_action, self.file_name, str(self.file_size), self.user]).encode('utf-8')
                        # 把file_name 从unicode编码为utf-8 进行比较操作
                        if self.sendhead(self.fhead) == self.file_name.encode('utf-8'):
                            self.sendfile()
                    else:
                        print '文件不存在,请重新操作.'
                elif self.file_action == 'get':
                    self.file_name = os.path.basename(self.file_path)
                    self.fhead = ' '.join([command,self.user])
                    self.file_size = self.sendhead(self.fhead)
                    if self.file_size == 'notexist':
                        print '文件不存在,请重新操作.'
                        self.sock.send('error')
                    else:
                        self.file_size = int(self.file_size)
                        self.recvfile()

if __name__ == '__main__':
    u = raw_input('请选择: 1(注册),2(登陆):')
    s = Userdo()
    if u == '1':
        if s.register():
            print '开始登陆...'
            user = s.login()
            if user:
                client = Socketclient('123.57.65.23', 10241, user)
                client.start()
    elif u == '2':
        user = s.login()
        if user:
            client = Socketclient('123.57.65.23',10241,user)
            client.start()
    else:
        print '输入错误'