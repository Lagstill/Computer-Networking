# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 14:04:02 2021

@author: 19PD05
"""

import socket
 
msgFromClient       = "8.8.8.8"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024
 
# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, 
                         type=socket.SOCK_DGRAM)
 
# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)
 
msgFromServer = UDPClientSocket.recvfrom(bufferSize)

msg = "Message from Server {}".format(msgFromServer[0])
print(msg)
