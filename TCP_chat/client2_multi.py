# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 10:00:25 2021

@author: 19PD05
"""

import socket

HEADER = 64
PORT = 65432
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "10.1.66.123"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

ms="Greetings! from Client 2"
while(ms!='stop'):
    send(ms)
    ms=input()
if(ms=='stop'):
    send(DISCONNECT_MESSAGE)
