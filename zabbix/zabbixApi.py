#coding:utf-8

import requests
import json

class MyZabbix:
    def __init__(self):
        self.url = "http://192.168.1.39/api_jsonrpc.php"
        self.data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": "admin",
                "password": "zabbix"
            },
            "id": 1
            }
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
            "Content-type":"application/json-rpc"
            }
        self.token = self.getRequest()["result"]

    def getRequest(self):
        self.sendData = json.dumps(self.data)
        req = requests.post(url=self.url,headers=self.headers,data=self.sendData)
        content = req.json()
        return content

    def getHost(self):
        if self.token:
            self.data["auth"] = self.token
            self.data["method"] = "host.get"
            self.data["params"] = {
                "output": [
                    "hostid",
                    "host"
                ],
                "selectInterfaces": [
                    "interfaceid",
                    "ip"
                ]
            }
            self.data["id"] = 2
            result = self.getRequest()
            return result
            
        else:
            raise KeyError("we have no token")

    def getMedia(self):
        if self.token:
            self.data["auth"] = self.token
            self.data["method"] = "usermedia.get"
            self.data["params"] = {
                "output": "extend"
            }
            self.data["id"] = 3
            result = self.getRequest()
            return result


if __name__ == "__main__":
    m = MyZabbix()
    print m.getMedia()
