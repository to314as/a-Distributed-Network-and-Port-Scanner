import socket

host_ip = '127.1.1.1'
dest_ports = [i for i in range(25524,25526)]

def bannergrabbing(addr, port):
 print("Gettig service information for port: ", port)
 socket.setdefaulttimeout(1)
 bannergrabber = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 try:
  bannergrabber.connect((addr, port))
  print(addr)
  bannergrabber.send('NothingToSee')
  banner = bannergrabber.recv(2048)
  bannergrabber.close()
  return 1,banner
 except:
  return 0,""
  
def main(dest_ip):
  dest_port=[dst.split(":")[1]]
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
          if response == 1:
              openp.append(port)
      if len(openp) != 0:
          print ("Possible Open or Filtered Ports:")
          print (openp)
      if len(openp) == 0:
          print ("No ports open")