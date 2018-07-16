#!/usr/bin/env python

from __future__ import print_function
import socket
import sys
from os import fork
from datetime import datetime
from os import getloadavg
import psutil

class TCPServer():
    
    def __init__(self,host,port,debug):
        self.debug = debug
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.server_address = (host,port)
        self.sock.bind(self.server_address)
        self.eprint('creating server on ip %s port %s' % self.server_address)
        self.eprint('waiting for client')
        self.sock.listen(1)
        self.connection = None
        self.client_address = None

    def eprint(self, x):
        if self.debug == 1:
            print(x, file=sys.stderr)

    def exit(self):
        self.connection.close()

    def date(self):
        self.eprint("date")
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S").encode('utf-8')
        
    def user(self):
        self.eprint("name of user")
        usr=[]
        for u in psutil.users():
            usr.append(u[0])
        return (" ".join(usr).encode('utf-8'))

    def top(self):
        self.eprint ("use of resources")
        return (str(getloadavg()).encode('utf-8'))


    def menu(self):
        menu = "\n\n \t MENU \n\n functions: \n date : current time \n user : username \n top : used resources \n exit : close connection \n"
        return menu.encode('utf-8')
    
    def get_request(self):
        #get function name from client
        choix = self.connection.recv(16)
        if choix:
            cmds = choix.decode()
            cmd = cmds.split(" ")[0].strip("\n")
        else:
            cmd = None
        return cmd

    def send_result(self,result):
        #result is sent to client
        self.connection.sendall(result)
    
    commandes  = {
        "date" : date,
        "top" : top, 
        "user" : user,
        "menu" : menu,
        "exit" : exit,
    }

    def do_work(self):
        while True:
            self.connection, self.client_address = self.sock.accept()
            pid = fork()
            if pid == 0: 
                #nous somme dans le processus enfant
                self.eprint("child process")
                self.sock.close()
                try:
                    self.send_result(self.menu())
                    self.eprint("connection depuis %s sur le port %s"%(self.client_address[0],self.client_address[1]))
                    while True:
                        cmd = self.get_request()
                        if cmd is not None  and cmd != 'exit':
                            if cmd in self.commandes.keys():
                                res = self.commandes[cmd](self)
                            else:
                                res = "command not found".encode('utf-8')
                            self.send_result(res + "\n")
                        else:
                            print("closing the connection %s", self.client_address[0])
                            exit()
                except Exception as e:
                    print("ERROR!!! , error code %s" % str(e))
                finally:
                    self.connection.close()
                    exit()
            else:
                self.eprint("parent process")
                self.connection.close()
    
if __name__ == '__main__':
    serv = TCPServer('localhost',10000,1)
    serv.do_work()
