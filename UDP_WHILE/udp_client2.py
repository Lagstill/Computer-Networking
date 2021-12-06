# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 10:43:59 2021

@author: 19PD05
"""

import socket

server_addr=('127.0.0.1',20001)

UDP_client2=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

UDP_client2.sendto(b'Hello from client2', server_addr)
 
msgFromServer = UDP_client2.recvfrom(1024)
 
msg = "Message from Server {}".format(msgFromServer[0])
print(msg)
stop_msg="No more clients"
UDP_client2.sendto(stop_msg.encode('utf-8'),server_addr)