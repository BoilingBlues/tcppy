
#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# 文件名：client.py
 
 
import socket
 
s = socket.socket()
s.connect(('192.168.220.129',9999))  #连接服务端
while True:#
	data = input('data:')
	s.send(data.encode())#发送数据
	recv = s.recv(1024).decode()
	print(recv)
	if data=='close':
		break
s.close()