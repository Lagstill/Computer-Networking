# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 08:42:28 2021

@author: 19pd06
"""
#post request 
#curl -d "name=19PD05 -X POST http://192.168.43.147/
#curl -X PUT http://localhost:8000/ -d "19PD05"
#curl -X DELETE http://localhost:8000/index.html
import socket
import os

# Define socket host and port
SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 8000

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

while True:    
    # Wait for client connections
    client_connection, client_address = server_socket.accept()
    #print("Accepted")

    # Get the client request
    request = client_connection.recv(4000).decode()
    print(request)
    headers = request.split('\n')
    if "GET /" in headers[0]:
        # Get the content of the file
        filename = headers[0].split()[1]
        if filename == '/':
            filename = 'index.html'
        try:
            fin = open('C:/Users/kpdla/Documents/SEM5/HTTP Protocol/httpfile/'+filename)
            content = fin.read()
            fin.close()
            # Send HTTP response
            response = 'HTTP/1.0 200 OK\n\n'+ content
        except FileNotFoundError :
            fin = open('error.html')
            content = fin.read()
            fin.close()
            response = 'HTTP/1.0 200 OK\n\n'+ content
    elif "POST /" in headers[0]:
        response = 'HTTP/1.0 200 OK\n\n'+headers[-1]
    elif "PUT /" in headers[0]:
        file1 = open("db.txt", "a")  
        file1.write(headers[-1]+"\n")
        file1.close()
        response = 'HTTP/1.0 200 OK\n\nData is written using PUT request.'
    elif "DELETE /" in headers[0]:
        filename=headers[0].split('/')
        filename=filename[1]
        filename=filename.split(' ')[0]
        print(filename)
        try:
            os.remove(filename)
            response='HTTP/1.1 200 OK\n\nFile Deleted Successfully'
        except:
            response='HTTP/1.1 204 No Content\nFile Does not exist'
    client_connection.sendall(response.encode())
    client_connection.close()
# Close socket
server_socket.close()
                
                
                