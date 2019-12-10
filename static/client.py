#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import socket
from tcppy import client

PORT = 9999
BUFFER_SIZE = 1024


def client_start():
	sock = client(PORT,BUFFER_SIZE)
	while True:
		data = input('me:')
		if not data:
			print('input is empty')
		else:
			sock.send(data)
			recv = sock.receive()
			if not recv:
				print('server error')
			elif recv.split()[0]=='--sendfile':
				sock.file_received(recv)
			if data=='bye':
				sock.close()
				break
			print('server: ',recv)	
	sock.close()



if __name__=='__main__':
	client_start()