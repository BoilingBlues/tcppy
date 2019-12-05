#!/usr/bin/python3
# -*- coding: UTF-8 -*-
 
import socket
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #tcp/ip scoket
sock.bind(('127.0.0.1',9999)) 
sock.listen(128)
while True:
	print('wait client')
	client,addr = sock.accept()
	print('get client',addr)
	while True:
		data = client.recv(1024)
		data = data.decode()
		if not data or data=='bye':
			print('server closed',addr)
			client.close()
			break
		else:
			print('get', data)
			msg = input('return')
			client.send(msg.encode()) 
sock.close()
