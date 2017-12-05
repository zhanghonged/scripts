#coding:utf-8
import peewee

connect = peewee.MySQLDatabase(
    database = 'socket',
    host = '127.0.0.1',
    passwd = 'root',
    user = 'root',
    port = 3306
)


class User(peewee.Model):
    username=peewee.CharField(max_length=20)
    password=peewee.CharField(max_length=50)
    register_time=peewee.DateTimeField()
    class Meta:
        database=connect


class File_trans(peewee.Model):
    filename = peewee.CharField(max_length=50)
    filepath = peewee.CharField(max_length=200)
    filesize = peewee.IntegerField()
    action = peewee.CharField(max_length=10)
    user = peewee.CharField(max_length=20)
    ip = peewee.CharField(max_length=50)
    action_date = peewee.DateTimeField()
    class Meta:
        database = connect
if __name__ == '__main__':
    connect.create_tables([User,File_trans])