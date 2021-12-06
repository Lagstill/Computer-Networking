# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 14:42:51 2021

@author: Sabareesh
"""
import socket
import threading
import math
clientsockets=[]
mtuhost={}
hostname={}

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(("localhost",12345))
print("Listening on port 12345")
s.listen(5)

def handle_client(c):
    while True:
        msg=c.recv(1024)
        msg=msg.decode('ascii')
        print(msg)
        if "MTUCONFIG" in msg:
            mtuchange=msg.split(':')[1]
            mtuhost[c]=mtuchange
            print(mtuhost[c])
            c.send("MTU updated successfully".encode('ascii'))
        else:
            list1=msg.split(':')
            length=list1[0]
            destination=list1[1]
            donotfragment=int(list1[2])
            morefragment=list1[3]
            offset=list1[4]
            data=list1[5]
            #print(data)
            mtu=mtuhost[hostname[destination]]
            mtu=int(mtu)
            #print(mtu)
            length=len(data)
            if donotfragment and length>mtuhost[hostname[destination]]:
                c.send("Not able to send the data without fragmentation".encode('ascii'))
                continue
            start=0
            cnt=0
            #print(data[start:start+mtu-5])
            while(length!=0):
                tosend=""
                if length>mtu-5:
                    tosend+="13:"+destination+":0:1:"+str(cnt)+":"+str(data[start:start+mtu-5])
                    print(tosend)
                    start=start+mtu-5
                    length=length-(mtu-5)
                    cnt+=1
                else:
                    tosend+=str(length+5)+":"+destination+":0:0:"+str(cnt)+":"+data[start:start+length+1]
                    print(tosend)
                    length=0
                c.send(tosend.encode('ascii'))
            tosend="Message sent successfully to "+destination
            c.send(tosend.encode('ascii'))
    
while True:
    c,addr=s.accept()
    if c not in clientsockets:
        c.send("Enter Host Name:".encode('ascii'))
        name=c.recv(1024)
        name=name.decode('ascii')
        hostname[name]=c
        c.send("Enter MTU:".encode('ascii'))
        mtu=c.recv(1024)
        mtu=mtu.decode('ascii')
        clientsockets.append(c)
        mtuhost[c]=int(mtu)
        #print(mtuhost[c])
        print(name," connected to server")
        c.send("MTU set successfully".encode('ascii'))
        thread=threading.Thread(target=handle_client,args=(c,))
        thread.start()
s.close()
    