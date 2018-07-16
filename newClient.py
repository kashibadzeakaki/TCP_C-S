#!/usr/bin/env python
import socket
import sys
import os

class TCPclient():
    def __init__(self,ip,port):
        self.ip=ip
        self.port=int(port)
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address=(self.ip,self.port)
        self.sock.connect(self.server_address)
    

    def work(self):
        try:
            while True:
                data=self.sock.recv(8192)
                if data == "":
                    exit()
                print(data)
                req = raw_input()
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