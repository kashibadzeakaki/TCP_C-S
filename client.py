#!/usr/bin/env python
import socket
import sys
import os

class TCPclient():
    def __init__(self,ip,port):
        self.ip=ip
        self.port=int(port)
        #creating socket
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address=(self.ip,self.port)
        #connection to ip:port
        self.sock.connect(self.server_address)
    

    def work(self):
        try:
            #while works until user press ctrl+c or write exit, after exit server will close connection 
            while True:
                #getting data from server , max 2048 bytes 
                data=self.sock.recv(2048)
                if data == "":
                    exit()
                print(data)
                #waiting for user to enter next command name
                req = raw_input()
                #sending command name to server
                self.sock.sendall(req)
        except socket.timeout:
            print("sock.close()")
            self.sock.close()

if __name__ == '__main__':
    print("please enter ip address (localhost) ")
    ip=raw_input()
    print("please enter port number (10000)")
    port=raw_input()
    client = TCPclient(ip,port)
    client.work()
