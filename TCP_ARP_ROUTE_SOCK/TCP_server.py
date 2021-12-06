# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 09:18:22 2021

@author: 19PD05
"""

import socket
import os


HOST='10.1.66.123'
PORT=65432

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen()
    conn,addr=s.accept()
    with conn:
        print('Connected by',addr)
        while True:
            data=conn.recv(2048)
            print('Recieved from client',data)
            data=data.decode("utf-8") 
            if not data:
                break
            elif data=='R':
                stream = os.popen('route print')
                output = stream.read()
                print(output)
                res = bytes(output, 'utf-8')
            elif data=='S':
                stream = os.popen('netstat -s')
                output = stream.read()
                print(output)
                res = bytes(output, 'utf-8')
            elif data=='A':
                stream = os.popen('ARP -a')
                output = stream.read()
                print(output)
                res = bytes(output, 'utf-8')
            
            conn.sendall(res)

