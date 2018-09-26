#!/usr/bin/python
#coding:utf-8
import requests
import json
import sys

token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
send_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="

params = {
    "corpsecret":"xxxxxxxxxxxxxxxxxxxxxxxxxx",
    "corpid":"xxxxxxxxxxxxxxxxx"
}


def get_token():
    req = requests.get(url=token_url,params=params)
    #content = json.loads(req.content)
    content = req.json()
    return content['access_token']


def sendMsg(user,message):
    token = get_token()
    send_url1 = send_url + token

    send_data = {
        "touser": user,
        "msgtype": "text",
        "agentid": 1000002,
        "text": {
           "content": message
        },
        "safe":0
    }

    try:
        req = requests.post(url=send_url1,data=json.dumps(send_data))
    except Exception as e:
        print(str(e))
    else:
        content = req.content
        print(content)

if __name__ == "__main__":
    user = sys.argv[1]
    message = sys.argv[2]
    sendMsg(user,message)
