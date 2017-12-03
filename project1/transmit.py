#coding:utf-8

import time
import struct
import SocketServer
from model import File_trans


class MyHandel(SocketServer.BaseRequestHandler):
    def setup(self):
        pass

    def recev(self):
        fileinfo_size = struct.calcsize('128sl')
        self.buf = self.request.recv(fileinfo_size)
        if self.buf:
            self.filename, self.filesize = struct.unpack('128sl', self.buf)
            self.filename = self.filename.strip('\00')
            recev_size = 0
            file = open(self.filename, 'wb')
            print 'start..........'
            while not recev_size == self.filesize:
                if self.filesize - recev_size > 1024:
                    rdata = self.request.recv(1024)
                    recev_size += len(rdata)
                else:
                    rdata = self.request.recv(self.filesize - recev_size)
                    recev_size = self.filesize
                file.write(rdata)
            file.close()
            print 'receive done...'
            F = File_trans()
            F.filename = self.filename
            F.filesize = self.filesize
            F.action = 'upload'
            F.action_date = time.strftime('%Y-%m-%d %H:%M:%S')
            F.save()


    def handle(self):
        print 'connect from : %s %s' %self.client_address
        while True:
            self.recev()


    def finish(self):
        pass

if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer(('',10021),MyHandel)
    server.serve_forever()



