import socket
from scapy.layers.inet import *
from scapy.all import *

host_ip = '127.1.1.1'
dest_ports = [i for i in range(22000,23000)]

def bannergrabbing(host, port):
    banner=b''
    print("Gettig service information for port: ", port)
    socket.setdefaulttimeout(0.5)
    bannergrabber=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r=bannergrabber.connect_ex((host, port))
    if r==0:
      #bannergrabber.send(b'hi')
      #banner = bannergrabber.recv(2048)
      r=r
    bannergrabber.close()
    return r,banner

def main(dst):
  dest_ports=[dst.split(":")[1]]
  host_ip=dst.split(":")[0]
  openp=[]
  for port in dest_ports:
      response,banner = bannergrabbing(host_ip, port)
      print(banner)
      if response == 1:
          openp.append(port)
  if len(openp) != 0:
      print ("Possible Open or Filtered Ports:")
      print (openp)
  if len(openp) == 0:
      print ("No ports open")
  return openp
if __name__ == '__main__':
    openp=[]
    for port in dest_ports:
        response,banner = bannergrabbing(host_ip, port)
        print(banner)
        if response == 0:
            openp.append(port)
    if len(openp) != 0:
        print ("Possible Open or Filtered Ports:")
        print (openp)
    if len(openp) == 0:
        print ("No ports open")
