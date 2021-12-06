# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 10:41:50 2021

@author: 19PD05
"""


import socket

server_addr=('127.0.0.1',20001)
UDP_server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

UDP_server.bind(server_addr)
print("Server is ready")
flag=True
while(flag):
    bytesAddressPair = UDP_server.recvfrom(1024)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    
    print(clientMsg)
    print(clientIP)
    #print(clientMsg.decode('utf-8')=="No more clients")
    #print(clientMsg.endswith("No more clients"))
    if message.decode('utf-8')=="No more clients":
        print("Server closing")
        flag=False
        UDP_server.close()
    else:
        UDP_server.sendto(b'Hello from UDP server', address)