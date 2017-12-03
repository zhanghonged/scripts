#coding:utf-8
import peewee
import time

connect = peewee.MySQLDatabase(
    database = 'project1',
    host = '127.0.0.1',
    passwd = 'root',
    user = 'root',
    port = 3306
)


class File_trans(peewee.Model):
    filename = peewee.CharField(max_length=50)
    filesize = peewee.IntegerField()
    action = peewee.CharField(max_length=10)
    action_date = peewee.DateTimeField()
    class Meta:
        database = connect
if __name__ == '__main__':
    File_trans.create_table()