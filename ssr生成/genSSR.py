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
    test1 = "ssr://MS4yLjMuNDoyMzMzOmF1dGhfYWVzMTI4X21kNTphZXMtMTI4LWN0cjp0bHMxLjJfdGlja2V0X2F1dGg6Y0dGemMzZHZjbVF4Lz9vYmZzcGFyYW09JnByb3RvcGFyYW09JnJlbWFya3M9Jmdyb3VwPSZ1ZHBwb3J0PTAmdW90PTA"
    print(getConfig(test1))

    t2 = {'ip': '1.2.3.4', 'port': '2333', 'method': 'aes-128-ctr', 'passwd': 'password1', 'protocol': 'auth_aes128_md5', 'obfs': 'tls1.2_ticket_auth', 'type': 'ssr'}
    print(makeConfig(t2))
