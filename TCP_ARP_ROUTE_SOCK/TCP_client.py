# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 09:18:00 2021

@author: 19PD05
"""

import socket

HOST='10.1.66.123'
PORT=65432
opt1='R'
opt2='A'
opt3='S'

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    res = bytes(opt1, 'utf-8')
    s.sendall(res)
    data=s.recv(2048)
    
print('Recieved',repr(data))
s.close()