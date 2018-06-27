#!/usr/bin/python
#coding:utf-8
import requests
import sys
"""
亿互无线的短信平台
"""
host  = "http://106.ihuyi.com/webservice/sms.php?method=Submit"
 

account  = "xxx"
password = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
 

def send_sms(text, mobile):
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    params = {
        'account': account,
        'password' : password,
        'content': text,
        'mobile':mobile,
        'format':'json'
        }
    req = requests.post(url=host, headers=headers, params=params)
    content = req.content
    return content
 
if __name__ == '__main__':
    mobile = sys.argv[1]
    textList = sys.argv[2].split('+')
    if len(textList) == 5:
        action = textList[0]
        machine = textList[1]
        problem = textList[2]
        problem_date = "-".join(textList[3:5])
        text = "故障%s ,主机:%s,发送故障:%s,时间:%s." %(action,machine,problem,problem_date)
    else:
        action = textList[0]
        confirm_user = textList[1]
        confirm_date = "-".join(textList[2:4])
        confirm_msg = textList[4]
        machine = textList[5]
        problem = textList[6]
        text = "故障%s,确认人:%s,确认时间:%s,消息:%s.主机:%s,故障:%s." %(action,confirm_user,confirm_date,confirm_msg,machine,problem)
    print(send_sms(text, mobile))
