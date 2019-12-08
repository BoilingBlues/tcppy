# -*- coding: UTF-8 -*-
import socket
import os

class link():
    def __init__(self):
        self.session
    def send(self,message):
        self.session.send(message.encode())
    def receive(self):
        print('wait')
        return self.session.recv(self.BUFFER_SIZE).decode()
    def close(self):
        self.session.send('bye')
        print("session closed")


class client(link):
    def __init__(self,port,BUFFER_SIZE):
        server_ip = input("please input the server ip address:")
        self.session = socket.socket()
        self.session.connect((server_ip,port))
        self.BUFFER_SIZE = BUFFER_SIZE
        print("connected server,input --getfile filename to download file")

    def file_received(self,recv):
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
    

class server(link):
    def __init__(self,host,port,max_listen,buffer_size):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host,port))
        self.sock.listen(max_listen)
        self.BUFFER_SIZE = buffer_size
    def connect_client(self):
        print('wait client')
        self.session,self.client_addr = self.sock.accept()
        print('get client',self.client_addr)

    def file_send(self,data):
        filename = data.split()[1]
        if filename in os.listdir('./static/'):
            filesize = str(os.path.getsize(filename))
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
        self.sock.close()