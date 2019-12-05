
#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# 文件名：client.py
 
 
import socket
 
s = socket.socket()
s.connect(('127.0.0.1',9999))
while True:
	data = input('send out data:')
	s.send(data.encode())
	recv = s.recv(1024).decode()
	print('get',recv)
	if data=='close':
		break
s.close()
