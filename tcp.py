#学习https://blog.csdn.net/adwenwen/article/details/79031085；https://www.cnblogs.com/alben-cisco/p/7051286.html；https://blog.csdn.net/thare_lam/article/details/49506565；https://blog.csdn.net/mouday/article/details/79101951内容

###server：

# -*- coding: utf-8 -*-
from socket import *
import struct
import json
import os

tcp_server = socket(AF_INET, SOCK_STREAM)
ip_port = (('', 8080))#ip可为空/localhost/本机ip
buffsize = 1024

#   端口的重复利用
tcp_server.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
tcp_server.bind(ip_port)
tcp_server.listen(5)
print('未链接')

def funone():
    while True:
        '''链接循环'''
        conn, addr = tcp_server.accept()

        print('链接人的信息:', addr)
        while True:
            if not conn:#是否链接
                print('客户端链接中断')
                break
            '''通信循环'''
            filemesg = input('请输入要传送的文件名及后缀>>>').strip()

            filesize_bytes = os.path.getsize(filemesg) # 得到文件的大小,字节
            filename = 'new' + filemesg
            dirc = {
                'filename': filename,
                'filesize_bytes': filesize_bytes,
            }#定义文件名及大小
            head_info = json.dumps(dirc)  # 将字典转换成字符串
            head_info_len = struct.pack('i', len(head_info)) #  将字符串的长度打包
            conn.send(head_info_len)  # 发送head_info的长度
            conn.send(head_info.encode('utf-8'))

        #   发送信息
            with open(filemesg, 'rb') as f:
                data = f.read()
                conn.sendall(data)

            print('发送成功')

def funtwo():
    conn, addr = tcp_server.accept()#链接
    print('链接人的信息:', addr)
    while True:  
        data = conn.recv(1024)
        data = data.decode()#解码
        if not data:
            break
        print('recieved message:',data)
        send = input('return:')
        conn.sendall(send.encode())#再编码发送  

    conn.close()  
    tcp_server.close()

#菜单
if __name__=='__main__':
    print('传输文件请输入a，传输字符请输入b，退出请输入q')
    while True:
        command = input('>>')
        if command =="a":
            funone()#调用文件传输函数
        if command =="b":
            funtwo()#调用字符传输函数
        if command =="q":
            break#退出


###client：
# -*- coding: utf-8 -*-
from socket import *
import struct
import json
import os
import sys
import time

tcp_client = socket(AF_INET, SOCK_STREAM)
ip_port = (('', 8080))#填写服务器端ip
buffsize = 1024
tcp_client.connect_ex(ip_port)
print('等待链接服务端')
# 文件传输
def funo():
    while True:
        head_struct = tcp_client.recv(4)  # 接收报头的长度,
        if head_struct:
            print('已连接服务端,等待接收数据')
        head_len = struct.unpack('i', head_struct)[0]  # 解析报头字符串大小
        data = tcp_client.recv(head_len)  # 接收长度为head_len的报头内容的信息 (包含文件大小,文件名的内容)

        head_dir = json.loads(data.decode('utf-8'))
        filesize_b = head_dir['filesize_bytes']
        filename = head_dir['filename']

        #   接收文件内容
        recv_len = 0
        recv_mesg = b''
        old = time.time()#当前时间
        f = open(filename, 'wb')
        while recv_len < filesize_b:
            percent = recv_len / filesize_b#接收比例

            if filesize_b - recv_len > buffsize:

                recv_mesg = tcp_client.recv(buffsize)
                f.write(recv_mesg)
                recv_len += len(recv_mesg)
            else:
                recv_mesg = tcp_client.recv(filesize_b - recv_len)
                recv_len += len(recv_mesg)
                f.write(recv_mesg)#写入文件大小、内容

        print(recv_len, filesize_b)#输出文件字节数
        now = time.time()#用时计算
        stamp = int(now - old)
        print('总共用时%ds' % stamp)#输出用时
        f.close()
#接收完成

def funt():
    while True:  
        trigger = input("send:")  
        tcp_client.sendall(trigger.encode())  
        data = tcp_client.recv(1024)  
        data = data.decode()  #解码
        print('recieved:',data)  
        if trigger.lower() == '1':#发送1结束连接  
            break  
    tcp_client.close()

if __name__=='__main__':
    while True:
        command = input('>>')
        if command =="a":
            funo()#传输文件
        if command =="b":
            funt()#传输字符
        if command =="q":
            break#退出