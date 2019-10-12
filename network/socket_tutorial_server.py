import socket
import time
import argparse
HOST = '127.0.0.2'  # Standard loopback interface address (localhost)
parser = argparse.ArgumentParser(description='Argumetns for client program')
parser.add_argument('-p', type=int, default=9999, help='the port of the receiver')
args = parser.parse_args()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, args.p))
    s.listen()
    while True:
        conn, addr = s.accept()
        if(conn):
            print('Connected by', addr)
        data = conn.recv(1024)
        if(data):
            #for i in range(0,10):
            #    time.sleep(1)
            print(data)