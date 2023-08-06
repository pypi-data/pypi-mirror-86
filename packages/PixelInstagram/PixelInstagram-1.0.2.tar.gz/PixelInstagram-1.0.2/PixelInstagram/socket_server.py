#!/usr/bin/env python
# coding: utf-8


from socket import *
import json

# 维护一个字典 key 是uid   value 是[ip,port] - server端口
user_dict = {}

HOST = ''
PORT = 21567
BUFSIZ = 1024


def run_server(host=HOST, port=PORT):

    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind((host, port))
    tcpSerSock.listen(5)


    while True:
        print('waiting for connection...')
        tcpCliSock, addr = tcpSerSock.accept()
        print('...connnecting from:', addr)

        while True:
            data = tcpCliSock.recv(BUFSIZ)
            #    [ flag,user1_name,user2_name,data]
            #    1是发送消息 0是获取用户列表
            if not data:
                break
            data = json.loads(data)
            print(data)
            if data[0] == 1:
                msg_sender = data[1]
                msg_receiver = data[2]
                msg_data = data[3]
                #         msg格式 [sender_name , data]
                msg = []
                msg.append(msg_sender)
                msg.append(msg_data)
                msg = json.dumps(msg)
                receiver_addr = user_dict[data[2]]
                print(receiver_addr)
                addr = (receiver_addr[0], receiver_addr[1])
                tcp_CliSock = socket(AF_INET, SOCK_STREAM)
                tcp_CliSock.connect(addr)
                tcp_CliSock.send(msg.encode())
                tcp_CliSock.close()

            else:
                user_name = data[1]
                if user_name in user_dict:
                    user_dict[user_name] = [data[2], data[3]]
                    print(user_dict[user_name])
                    data = json.dumps(list(user_dict.keys()))
                    tcpCliSock.send(data.encode())
                else:
                    msg = "user_name error"
                    data = json.dumps(msg)
                    tcpCliSock.send(data.encode())
        tcpCliSock.close()
    tcpSerSock.close()
