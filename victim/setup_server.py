import sys
import socket
import select
import numpy as np

if len(sys.argv) <= 1:
    ports = [55555]
else:
    ports = sys.argv[2:-2]

HOST = '127.1.1.1'
servers = []
print(ports)
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
        print('Connected by', address)
        while True:
            data = connection.recv(1024)
            if data:
              print(data)
              connection.send(data)
            connection, address = ready_server.accept()