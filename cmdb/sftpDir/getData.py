#!/usr/bin/python
# coding:utf-8

import uuid, platform


def get_hostname():
    hostname = platform.node()
    return hostname


# def get_system():
#     system = platform.platform()
#     return system

def get_systemVersion():
    sys_version = ''
    with open('/etc/issue') as fd:
        for line in fd:
            sys_version = line.strip()
            break
    return sys_version

def get_systeType():
    sys_type = platform.system()
    return sys_type

def get_mac():
    uid = uuid.UUID(int=uuid.getnode()).hex[-12:]
    mac = ":".join([uid[e:e + 2] for e in range(0, 11, 2)])
    return mac

def get_cpu():
    num = 0
    cpu_model = ''
    with open('/proc/cpuinfo') as fd:
        for line in fd:
            if line.startswith('processor'):
                num += 1
            if line.startswith('model name'):
                cpu_model = line.split(':')[1].strip().split()
                cpu_model = cpu_model[0] + ' ' + cpu_model[2]  + ' ' + cpu_model[-1]
    cpu =  cpu_model + ' ' + str(num) + '核'
    return cpu
def get_memory():
    with open('/proc/meminfo') as fd:
        for line in fd:
            if line.startswith('MemTotal'):
                mem = int(line.split()[1].strip())
                break
    mem = '%.f' % (mem / 1024.0) + ' MB'
    return mem

if __name__ == "__main__":
    print get_hostname()
    print get_systemVersion()
    print get_mac()
