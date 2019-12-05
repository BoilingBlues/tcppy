#!/usr/bin/python3
# -*- coding: UTF-8 -*-
 
import socket
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #建立一个tcp/ip scoket
sock.bind(('127.0.0.1',9999)) #绑定端口号
sock.listen(128)#监听,同时能连多少个客户端
while True:
	print('开始等待下一个客户端过来。。。')
	client,addr = sock.accept() #接收到客户端的socket，和地址
	print('接收到 client数据',addr)
	while True:
		#
		data = client.recv(1024)#获取到客户端的数据
		data = data.decode()
		if not data or data=='bye':
			#如果没有发送过来数据就代表客户端close了，或者发过来bye代表连接要断开
			print('服务结束',addr)
			client.close()#断开连接，为下一个服务
			break
		else:#如果他还在发送的话
			print('发过来的', data)
			msg = input('回复：')
			client.send(msg.encode())  # 数据
sock.close()