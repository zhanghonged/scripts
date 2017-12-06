#coding:utf-8

import os
import socket

class Socketclient(object):
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((self.host,self.port))

    def register(self):
        self.username = raw_input('输入用户名:')
        data = ' '.join(['register',self.username])
        self.sock.send(data)
        rdata = self.sock.recv(512)
        if rdata == 'exists':
            print '用户名已存在.'
            return False
        elif rdata == 'ok':
            self.password = raw_input('输入密码:')
            if self.password.isalnum() and len(self.password) >= 6:
                self.password2 = raw_input('再次输入密码:')
                if self.password == self.password2:
                    self.sock.send(self.password)
                    self.sock.recv(512)
                    print '注册成功,请进行登录操作.'
                    return True

    def login(self):
        self.username = raw_input('username:')
        data = ' '.join(['login',self.username])
        self.sock.send(data)
        rdata = self.sock.recv(512)
        if rdata == 'exists':
            self.password = raw_input('输入密码:')
            self.sock.send(self.password)
            result = self.sock.recv(512)
            if result == 'success':
                print '登录成功.'
                return self.username
        else:
            print '用户名不存在！'
            return False

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

    def start(self,username):
        self.user = username
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
    client = Socketclient('localhost', 10021)
    u = raw_input('请选择: 1(注册),2(登陆):')
    if u == '1':
        s = client.register()
        if s:
            t = client.login()
            if t:
                client.start(t)
    elif u == '2':
        t = client.login()
        if t:
            print t
            client.start(t)
    else:
        print '输入错误！'