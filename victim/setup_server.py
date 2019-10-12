import sys
import socket
import select
import numpy as np

if len(sys.argv) <= 1:
    ports = 'default_container_name'
else:
    ports = sys.argv[1][1:-1].split(',')

HOST = '127.1.1.1'
servers = []
for port in ports:
    print(port)
    ds = (HOST, int(port))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(ds)
    server.listen(10)
    servers.append(server)

while True:
    readable,_,_ = select.select(servers, [], [])
    ready_server = readable[0]
    connection, address = ready_server.accept()
    with connection:
        print('Connected by', addr)
        while True:
            data = connection.recv(1024)
            if not data:
                break
            connection.sendall(data)