# -*- coding: UTF-8 -*-
import socket
import os
from Crypto.Cipher import AES
from Crypto.Random import random


class link():
    """
        Abstract base class
    """

    def send(self,message):
        """send message for client and server"""
        paddingLength = 16 - len(message) % 16
        paddingByte = chr(paddingLength)
        message = message + paddingByte * paddingLength
        message = self.aes.encrypt(message.encode())
        self.session.send(message)

    def receive(self):
        """receive message for client and server"""
        print('wait')
        message = self.session.recv(self.BUFFER_SIZE).strip()
        message = self.aes1.decrypt(message).decode()
        if(len(message) % 16 != 0):
            raise Exception("Error: length of the message should be multiple of 16!")
        paddingLength = ord(message[-1])
        message = message[ : -paddingLength]
        return message
        
    def close(self):
        """close the session"""
        self.send('bye')
        print("session closed")


class client(link):
    """
        the class of the client
    """
    def __init__(self,port,BUFFER_SIZE):
        server_ip = input("please input the server ip address:")
        self.session = socket.socket()
        self.session.connect((server_ip,port))
        self.BUFFER_SIZE = BUFFER_SIZE
        self.identity_verification()
        print("connected server,input --getfile filename to download file")

    def file_received(self,recv):
        """receive file from server"""
        self.session.send("File size received".encode())
        file_total_size = int(recv.split()[1])
        received_size = 0
        f = open("new" + recv.split()[2] ,"wb")
        while received_size < file_total_size:
            data = self.session.recv(self.BUFFER_SIZE)
            f.write(data)
            received_size += len(data)
            print("get:",received_size)
        f.close()
        print("receive done",file_total_size," ",received_size)   

    def genKey(self):
        """Randomly generate a private key"""
        key = ""
        H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        for i in range(16):
            key += random.choice(H)
        return key

    def identity_verification(self):
        """identity_verification for server"""
        key = self.genKey()
        iv = self.genKey()
        self.aes = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
        self.aes1 = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
        message = "key:" + key + ";iv:" + iv
        self.session.send(message.encode())
        ok_key = self.receive()
        if ok_key != "ok":
            print("identity verification error")
            self.close()
    

class server(link):
        """the class for server"""
    def __init__(self,host,port,max_listen,buffer_size):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host,port))
        self.sock.listen(max_listen)
        self.BUFFER_SIZE = buffer_size

    def connect_client(self):
        """wait to connect client"""
        print('wait client')
        self.session,self.client_addr = self.sock.accept()
        self.wait_identity_verification()
        print('get client',self.client_addr)

    def file_send(self,data):
        """send file to client"""
        filename = data.split()[1]
        if filename in os.listdir('./static/'):
            filesize = str(os.path.getsize('./static/'+filename))
            print("file's size：",filesize,filename)
            filemessage = '--sendfile '+filesize+' '+filename
            self.session.send(filemessage.encode())
            data = self.session.recv(self.BUFFER_SIZE)  
            print("send begin..")
            f = open('./static/'+filename, "rb")
            for line in f:
                self.session.send(line)
            f.close()
            print("send finished")
        else:
            self.session.send("0001".encode())   

    def server_close(self):
        """close the whole server"""
        self.sock.close()
    
    def wait_identity_verification(self):
        """"Complete authentication with client"""
        message = self.session.recv(self.BUFFER_SIZE).decode()
        key = message[4:20].encode()
        iv = message[24:].encode()
        self.aes = AES.new(key,AES.MODE_CBC,iv)
        self.aes1 = AES.new(key,AES.MODE_CBC,iv)
        self.send('ok')
    





