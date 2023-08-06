#!/usr/bin/env python
# coding: utf-8

import json
import threading
from socket import *

SERVER_IP = '127.0.0.1'  # or 'localhost'
SERVER_PORT = 21567

HOST_IP = ''
USER_PORT = 9992
BUFSIZ = 1024
ADDR1 = (SERVER_IP, SERVER_PORT)
ADDR2 = (HOST_IP, USER_PORT)

def send_msg(host, port):

    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect((host, port))
    data2 = input('>')
    data1 = [1, 'liu', 'meng']
    data1.append(data2)
    data1 = json.dumps(data1)
    tcpCliSock.send(data1.encode())
    tcpCliSock.close()
    return

def get_user_list(host, port):

    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect((host, port))
    data1 = [0]
    data2 = input('>')
    data1.append(data2)
    data3 = '0.0.0.0'
    data1.append(data3)
    data4 = input('>')
    data1.append(data4)
    data1 = json.dumps(data1)
    tcpCliSock.send(data1.encode())
    data1 = tcpCliSock.recv(BUFSIZ)
    data1 = json.loads(data1)
    print(data1)
    tcpCliSock.close()
    return data1


# 这里是开启一个监听端口
def User_Receive():
    global ADDR2
    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind(ADDR2)
    tcpSerSock.listen(5)

    while True:
        print('waiting for connection...')
        tcpCliSock, addr = tcpSerSock.accept()
        print('...connecting from:', addr)

        while True:
            data = tcpCliSock.recv(BUFSIZ)
            if not data:
                break
            data = json.loads(data)
            print(data[0] + ':' + data[1])
        tcpCliSock.close()
    tcpSerSock.close()


def run_client(port=SERVER_PORT, host=SERVER_IP):

    thread = threading.Thread(target=User_Receive)
    thread.start()
    while True:
        s = input('>-------------------'
                  '1. get_user_list'
                  '2. send_message')
        if s == '1':
            a = get_user_list(host, port)
        else:
            send_msg(host, port)

