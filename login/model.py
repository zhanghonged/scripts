#conding:utf-8
import peewee

connect=peewee.SqliteDatabase('account.db')

class User(peewee.Model):
    username=peewee.CharField(max_length=20)
    password=peewee.CharField(max_length=20)
    register_time=peewee.DateTimeField()
    class Meta:
        database=connect

if __name__ == '__main__':
    User.create_table()