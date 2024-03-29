#!/usr/bin/python3
# -*- coding: UTF-8 -*-
 
import socket
from tcppy import server

"""Parameter configuration"""
HOST = '0.0.0.0'
PORT = 9999
BUFFER_SIZE = 1024
MAX_LISTEN = 10


def server_start():
	sock = server(HOST,PORT,MAX_LISTEN,BUFFER_SIZE)
	while True:
		sock.connect_client()
		while True:
			data = sock.receive()
			print('client'+sock.client_addr[0]+':', data)
			if not data or data=='bye':
				sock.close()
				break
			else:
				if data.split()[0] == '--getfile':
					sock.file_send(data)
					continue
				msg = input('me:')
				if not msg:
					print('input is empty')
				elif msg =='bye':
					sock.close()
				else:
					sock.send(msg)
		
	sock.server_close()


if __name__ == "__main__":
	server_start()		