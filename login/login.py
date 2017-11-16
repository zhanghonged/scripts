#coding:utf-8
import base64
import random
import string
import hashlib
import datetime
from model import User


def movencry(p):
    p_list=list(p)
    template=string.printable
    num=random.choice(range(len(p_list)))
    s=p_list[num]
    if s.isupper():
        p_list[num]=template[template.index(s)-20].swapcase()
        p_list.append('-')
    elif s.islower():
        p_list[num]=template[template.index(s)+20].swapcase()
        p_list.append('+')
    return str(num) + '#'+ base64.encodestring(''.join(p_list))


def movdecry(passwd):
    template = string.printable
    num=int(passwd.split('#')[0])
    p_list=list(base64.decodestring(passwd.split('#')[1]))
    if p_list[-1] == '+':
        p_list[num] = template[template.index(p_list[num].swapcase()) - 20]
    elif p_list[-1] == '-':
        p_list[num] = template[template.index(p_list[num].swapcase()) + 20]
    p_list.pop()
    return ''.join(p_list)


##md5加密
def encry(p):
    serc=hashlib.md5('加密')
    serc.update(p)
    return serc.hexdigest()

def sign():
    username=raw_input('Enter username:')
    try:
        user=User.get(User.username==username)
    except:
        user=User()
        password=raw_input('Enter password:')
        if password.isalnum() and len(password) >= 6:
            password2=raw_input('Enter password again:')
            if password == password2:
                user.username = username
                user.password = encry(password)
                user.register_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                user.save()
                print 'sign successfully.'
            else:
                print 'The two passwords don\'t same!'
        else:
            print 'Must include Numbers and letters, and length is greater than 6!'
    else:
        print 'username already exists!'


def login():
    username=raw_input('username:')
    try:
        user=User.get(User.username==username)
    except:
        print 'username does not exist!'
    else:
        password = encry(raw_input("password:"))
        for i in range(2):
            if password == user.password:
                print 'login Success.'
                break
            else:
                password=encry(raw_input('password error, please re-enter:'))
                if password == user.password:
                    print 'login Success.'
                    break
        else:
            print 'More than three times. Please Just a moment.'

if __name__ == '__main__':
	a=raw_input('Select: 1(Sign),2(Login):')
	if a == '1':
		sign()
	elif a == '2':
		login()
	else:
		print 'Invalid input'