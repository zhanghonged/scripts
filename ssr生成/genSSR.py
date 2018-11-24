# -*- coding: utf-8 -*-
import base64

def add_equal(string):
    """
    base64编码补全，补=
    """
    missing_padding = 4 - len(string) % 4
    if missing_padding:
        string += "="*missing_padding
    return string

def parse_ss(ss):
    result_ss = {
        "ip":"",
        "port":None,
        "method":"",
        "passwd":"",
        "protocol":"origin",
        "obfs":"plain",
        "type":"ss"
    }
    left,right = ss.split("@")[0],ss.split("@")[1]
    result_ss["ip"],result_ss["port"] = right.split(":")[0],right.split(":")[1]
    result_ss["method"], result_ss["passwd"] = left.split(":")[0],left.split(":")[1]
    return result_ss

def parse_ssr(ssr):
    result_ssr = {
        "ip":"",
        "port":None,
        "method":"",
        "passwd":"",
        "protocol":"",
        "obfs":"",
        "type":"ssr"
    }
    left = ssr.split("/?")[0]
    result_ssr["ip"] = left.split(":")[0]
    result_ssr["port"] = left.split(":")[1]
    result_ssr["protocol"] = left.split(":")[2]
    result_ssr["method"] = left.split(":")[3]
    result_ssr["obfs"] = left.split(":")[4]
    # print(left.split(":")[5])
    result_ssr["passwd"] = base64.b64decode(add_equal(left.split(":")[5]).replace('-','+').replace('_','/')).decode('utf8')

    return (result_ssr)

def getConfig(s):
    temp = s.split("://")
    config_type = temp[0]
    # 解码前把字符串中包含的 – 和 _ 字符，分别替换为 + 和 /
    config_info_base64 = add_equal(temp[1])

    try:
        config_info = base64.b64decode(config_info_base64.replace('-','+').replace('_','/'))
    except Exception as e:
        print(str(e))
    else:
        # print(config_info)
        if (len(config_type) == 2 and config_type == "ss"):
            config = parse_ss(config_info.decode('utf8'))
            return config
        elif (len(config_type) == 3 and config_type == "ssr"):
            config = parse_ssr(config_info.decode('utf8'))
            return config

def makeConfig(d):
    config_type = d['type']

    if (len(config_type) == 2 and config_type == "ss"):
        config_file = d['method'] + ":" + d['passwd'] + "@" + d['ip'] + ":" + d['port']
        # print(config_file)
        config_file_base64 = base64.b64encode(config_file.encode('utf8'))
        return "ss://"+config_file_base64.decode('utf8')

    if (len(config_type) == 3 and config_type == "ssr"):
        passwd_base64 = base64.b64encode(d['passwd'].encode('utf8'))
        config_file = d['ip'] + ":" + d['port'] + ":" + d['protocol'] + ":" + d['method'] + ":" + d['obfs'] + ":" + passwd_base64.decode('utf8') + "/?obfsparam=&protoparam=&remarks=&group=&udpport=0&uot=0"
        # print(config_file)
        config_file_base64 = base64.b64encode(config_file.encode('utf8'))
        return "ssr://"+config_file_base64.decode('utf8').strip('=')

if __name__ == "__main__":
    test = "ss://cmM0LW1kNTpoR2RMWGhiQUA0Ny44OS4yMjUuMTI2OjMwMDMz"
    test1 = "ssr://MTc2LjEyMi4xMzIuMTIwOjIzMzM6YXV0aF9hZXMxMjhfbWQ1OmFlcy0xMjgtY3RyOnRsczEuMl90aWNrZXRfYXV0aDpjR0Z6YzNkdmNtUXgvP29iZnNwYXJhbT0mcHJvdG9wYXJhbT0mcmVtYXJrcz0mZ3JvdXA9JnVkcHBvcnQ9MCZ1b3Q9MA"
    test2 = "ssr://MTc2LjEyMi4xMzIuMTIwOjIzMzQ6YXV0aF9hZXMxMjhfbWQ1OmFlcy0xMjgtY3RyOnRsczEuMl90aWNrZXRfZmFzdGF1dGg6Y0dGemMzZHZjbVF5Lz9vYmZzcGFyYW09JnByb3RvcGFyYW09JnJlbWFya3M9Jmdyb3VwPSZ1ZHBwb3J0PTAmdW90PTA"
    print(getConfig(test))
    print(getConfig(test1))
    print(getConfig(test2))

    t = {'ip': '47.89.225.126', 'port': '30033', 'method': 'rc4-md5', 'passwd': 'hGdLXhbA', 'protocol': 'origin', 'obfs': 'plain', 'type': 'ss'}
    t2 = {'ip': '176.122.132.120', 'port': '2333', 'method': 'aes-128-ctr', 'passwd': 'password1', 'protocol': 'auth_aes128_md5', 'obfs': 'tls1.2_ticket_auth', 'type': 'ssr'}
    t3 = {'ip': '176.122.132.120', 'port': '2334', 'method': 'aes-128-ctr', 'passwd': 'password2', 'protocol': 'auth_aes128_md5', 'obfs': 'tls1.2_ticket_fastauth', 'type': 'ssr'}
    print(makeConfig(t))
    print(makeConfig(t2))
    print(makeConfig(t3))