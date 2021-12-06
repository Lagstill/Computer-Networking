# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 14:15:17 2021

@author: 19PD05
"""

import socket
import os

localIP     = "10.1.66.116"
localPort   = 20001
bufferSize  = 1024
 

 
# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, 
                    type=socket.SOCK_DGRAM)
 
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
 
print("UDP server up and listening")
 
# Listen for incoming datagrams 
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
   #clientMsg = "Message from Client:{}".format(message)
    ip_list=[]
    ip_list.append(message.decode("utf-8"))
    for ip in ip_list:
        response = os.popen(f"ping {ip}").read()
        if "Received = 4" in response:
            msgFromServer       = f"UP {ip} Ping Successful"
            bytesToSend = str.encode(msgFromServer)
            print(f"UP {ip} Ping Successful")
        else:
            msgFromServer       = f"UP {ip} Ping UNsuccessful"
            bytesToSend = str.encode(msgFromServer)
            print(f"DOWN {ip} Ping Unsuccessful")
    #lientIP  = "Client IP Address:{}".format(address)
    
   #print(clientMsg)
   #print(clientIP)
   
    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)

