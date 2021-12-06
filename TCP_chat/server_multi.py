# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 08:40:35 2021

@author: kpdla


import socket
import threading

HEADER=64
PORT=5050

SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)
FORMAT='utf-8'
DISCONNECT_MESSAGE="!DISCONNECT"

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected. ")
    
    connected=True
    while connected:
        msg_length=conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            #msg_length = len(msg_length)#int(msg_length).decode(FORMAT)
            msg=str(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected=False
                
            print(f"[{addr}] {msg}")
            conn.send("Server Msg recieved".encode(FORMAT))
            
    conn.close()
    
def start():
    server.listen(5)
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn,addr =server.accept()
        thread=threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
    

print("[STRATING] server is starting... ")
start()
"""

import socket 
import threading

HEADER = 64
PORT = 65432


SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            mg=input()
            conn.send(mg.encode(FORMAT))

    conn.close()
        

def start():
    server.listen(5)
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        

print("[STARTING] server is starting...")
start()
    