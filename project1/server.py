#coding:utf-8


import os
import time
import hashlib
import SocketServer
from model import File_trans,User


def log_decorator(fun):
    def wrapper(self):
        fun(self)
        F = File_trans()
        F.filename = self.file_name
        F.filepath = self.file_path
        F.filesize = self.file_size
        F.action = self.file_action
        F.user = self.user
        F.ip = self.ip
        F.action_date = time.strftime('%Y-%m-%d %H:%M:%S')
        F.save()
    return wrapper

class MyHandel(SocketServer.BaseRequestHandler):

    def encry(self,password):
        serc=hashlib.md5('加密')
        serc.update(password)
        return serc.hexdigest()


    def register(self):
        try:
            #若用户名能查到
            user = User.get(User.username == self.username)
            self.request.send('exists')
        except:
            #若查不到
            self.request.send('ok')
            self.password = self.request.recv(512)
            user = User()
            user.username = self.username
            user.password = self.encry(self.password)
            user.register_time = time.strftime('%Y-%m-%d %H:%M:%S')
            user.save()
            self.request.send('success')
    def login(self):
        try:
            user = User.get(User.username == self.username)
            self.request.send('exists')
        except:
            self.request.send('no')
        else:
            self.password = self.encry(self.request.recv(512))
            print self.password
            if self.password == user.password:
                self.request.send('success')

    def sendhead(self,head):
        self.request.send(head)
        rdata = self.request.recv(512)
        return rdata

    @log_decorator
    def sendfile(self):
        with open(self.file_path,'rb') as f:
            while True:
                data =f.read(1024)
                if not data:
                    break
                self.request.send(data)

    @log_decorator
    def recevfile(self):
        recev_size = 0
        file = open(self.file_path, 'wb')
        self.request.send(self.file_name)
        print 'start recv %s..........'%self.file_name
        while not recev_size == self.file_size:
            if self.file_size - recev_size > 1024:
                rdata = self.request.recv(1024)
                recev_size += len(rdata)
            else:
                rdata = self.request.recv(self.file_size - recev_size)
                recev_size = self.file_size
            file.write(rdata)
        file.close()
        print 'receive %s done...' %self.file_name

    def handle(self):
        print 'connect from : %s %s' %self.client_address
        self.ip = self.client_address[0]
        while True:
            self.buf = self.request.recv(1024)
            if self.buf:
                print self.buf
                if self.buf.startswith('get ',0,4) or self.buf.startswith('put ',0,4):
                    self.file_action = self.buf.split()[0]
                    if self.file_action == 'put':
                        self.file_name = self.buf.split()[1]
                        self.file_size = int(self.buf.split()[2])
                        self.user = self.buf.split()[3]
                        # 如果在linux环境 下面修改为os.path.dirname(__file__).decode('utf-8')
                        self.file_path = os.sep.join([os.path.dirname(__file__).decode('gbk'),self.file_name.decode('utf-8')])
                        self.recevfile()

                    elif self.file_action == 'get':
                        self.file_path = self.buf.split()[1].decode('utf-8')
                        self.user = self.buf.split()[2]
                        self.file_name = os.path.basename(self.file_path)

                        if os.path.isfile(self.file_path):
                            self.file_size = os.path.getsize(self.file_path)
                            if self.sendhead(str(self.file_size)) == 'begin':
                                self.sendfile()
                        else:
                            head = 'notexist'
                            self.sendhead(head)

                elif self.buf.startswith('register'):
                    self.username = self.buf.split()[1]
                    self.register()
                elif self.buf.startswith('login'):
                    self.username = self.buf.split()[1]
                    self.login()
                else:
                    break
            else:
                break


if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer(('',10021),MyHandel)
    server.serve_forever()