#!/usr/bin/python
# coding:utf-8

import uuid, platform


def get_hostname():
    hostname = platform.node()
    return hostname


def get_system():
    system = platform.platform()
    return system


def get_mac():
    uid = uuid.UUID(int=uuid.getnode()).hex[-12:]
    mac = ":".join([uid[e:e + 2] for e in range(0, 11, 2)])
    return mac


if __name__ == "__main__":
    print get_hostname()
    print get_system()
    print get_mac()
