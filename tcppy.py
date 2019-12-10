# -*- coding: UTF-8 -*-
import socket
import os
from Crypto.Cipher import AES
from Crypto.Random import random
from rsaPy import rsaPy


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
        message = self.session.recv(self.BUFFER_SIZE)
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
        try:
            self.identity_verification()
        except:
            print("identity verification error,lan is not safe")
            self.close()
        print("connected server,input --getfile filename to download file")

    def file_received(self,recv):
        """receive file from server"""
        self.send("File size received")
        file_total_size = int(recv.split()[1])
        received_size = 0
        f = open("new" + recv.split()[2] ,"w")
        while received_size < file_total_size:
            data = self.receive()
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
        self.rsa_consult(message)
        ok_key = self.receive()
        if ok_key != iv:
            print("identity verification error,server is not safe")
            self.close()
        self.passwd_confirm()

    def passwd_confirm(self):
        passwd = input("Enter password:")
        self.send(passwd)


    def rsa_consult(self,message):
        publickey = self.session.recv(self.BUFFER_SIZE)
        rsa_py = rsaPy()
        en_privatekey = rsa_py.encrypt(message.encode(),publickey)
        self.session.send(en_privatekey)

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
        try:
            self.wait_identity_verification()
        except:
            print("identity verification error,lan is not safe")
            self.close()
        print('get client',self.client_addr)

    def file_send(self,data):
        """send file to client"""
        filename = data.split()[1]
        if filename in os.listdir('./static/'):
            filesize = str(os.path.getsize('./static/'+filename))
            print("file's size：",filesize,filename)
            filemessage = '--sendfile '+filesize+' '+filename
            self.send(filemessage)
            data = self.receive()  
            print("send begin..")
            f = open('./static/'+filename, "r")
            for line in f:
                self.send(line)
            f.close()
            print("send finished")
        else:
            self.send("0001")   

    def server_close(self):
        """close the whole server"""
        self.sock.close()
    
    def wait_identity_verification(self):
        """"Complete authentication with client"""
        message = self.rsa_consult().decode()
        key = message[4:20].encode()
        iv = message[24:].encode()
        self.aes = AES.new(key,AES.MODE_CBC,iv)
        self.aes1 = AES.new(key,AES.MODE_CBC,iv)
        self.send(iv.decode())
        a = self.passwd_confirm()
        if not a:
            print("identity verification error,lan is not safe")
            self.close()
    
    def rsa_consult(self):
        """"send the public key to client,and get the aes/cbc private key"""
        rsa_py = rsaPy()
        self.session.send(rsa_py.pubkey)
        en_privatekey = self.session.recv(self.BUFFER_SIZE)
        privatekey = rsa_py.decrypt(en_privatekey)
        return privatekey

    def passwd_confirm(self):
        passwd = self.receive()
        f = open('user','r')
        for line in f:
            if line == passwd:
                return True
        return False

        





