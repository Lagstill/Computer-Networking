# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 08:58:54 2021

@author: 19pd05
"""

import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.43.147', 8000)
client_socket.connect(server_address)

request_header = 'GET / HTTP/1.0\r\njsonplaceholder.typicode.com/todos/1\r\n\r\n'
client_socket.send(bytes(request_header.encode()))

response = ''
#while True:
recv = client_socket.recv(4096)
"""
    if not recv:
        break
    response += recv """

print (recv.decode())
client_socket.close()    
