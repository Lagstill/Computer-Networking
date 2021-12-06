# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 10:43:26 2021

@author: 19PD05
"""

import socket

server_addr=('127.0.0.1',20001)

UDP_client1=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

UDP_client1.sendto(b'Hello from client1', server_addr)
 
msgFromServer = UDP_client1.recvfrom(1024)
 
msg = "Message from Server {}".format(msgFromServer[0])
print(msg)