# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 15:09:59 2021

@author: Sabareesh
"""

import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("--------IP FRAGMENTATION----------\n\n")
s.connect(("localhost",12345))
print("\n\tConnected Succesfully")
cnt=0
while True:
    if cnt==0:
        msg=s.recv(1024)
        print(msg.decode('ascii'),end="")
        tosend=input()
        s.send(tosend.encode('ascii'))
        msg=s.recv(1024)
        print(msg.decode('ascii'),end="")
        tosend=input()
        s.send(tosend.encode('ascii'))
        cnt+=1
        msg=s.recv(1024).decode('ascii')
        print(msg)
        continue
    inp=input("\nEnter The command\n\t1.MTUCONFIG:\n\t2.Send Data:\nFormat:Total Length:Host:DoNotFragment:MoreFragment:Offset:Data\n")
    s.send(inp.encode('ascii'))
    msg=s.recv(1024).decode('ascii')
    while ":" in msg:
        print(msg)
        msg=s.recv(1024).decode('ascii')
    print(msg)
    inp=input("Do you want to continue:(y/n)")
    if inp=="n":
        break
    