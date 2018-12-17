#!/usr/bin/env python
#-*- coding:utf-8 -*-

from socket import*  

HOST = '127.0.0.1'    # The remote host  
PORT = 6666                 # The same port as used by the server  
s = None

def startClient():
    BUFSIZE = 1024  
    ADDR = (HOST, PORT)  

    while True:  
        data = input('> ')
        if not data:
            break  
        tcpCliSock = socket(AF_INET, SOCK_STREAM)  
        tcpCliSock.connect(ADDR)  
        tcpCliSock.send(data.encode())  
        data = tcpCliSock.recv(BUFSIZE).decode()  
        # print(data)
        tcpCliSock.close()  
        target = open(data,"r")
        buffer = target.readlines()
        for line in buffer:
            print line

if __name__ == "__main__":
    root = startClient()
    root.mainloop()