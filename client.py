#!/usr/bin/env python
import socket
import sys
import os

def scanport():
    print("input port number")
    port=raw_input()
    return int(port)

def scanip():class TCPClient():
    print("which ip you want to connect")
    ip=raw_input()
    return ip

def print_data(data):
    print>>sys.stderr, 'data received from server:  %s' % data

def get_data(conn):
    """
    Recevoir des donnees depuis le serveur
    """
    data=conn.recv(8192)
    if data == "":
        print("Connection closed")
        exit()
    return (data)

def get_req():
    """
    Recuperer a la ligne de commande le choix de l'utilisateur
    """
    method=raw_input()
    if method == None:
        return None
    else:
        return method

def send_choice(chc,sock):
    """
    Envoie le choix de l'utilisateur au serveur
    """
    sock.sendall(chc)

port=port()
ip=ip()
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address=(ip,port)
print>>sys.stderr, 'Connexion vers %s sur le port %s'% server_address
sock.connect(server_address)

try:
    while True:
        data=get_data(sock)
        print_data(data)
        req=get_req()
        send_choice(req,sock)
except socket.timeout:
    print("sock.close()")
    sock.close()

    

