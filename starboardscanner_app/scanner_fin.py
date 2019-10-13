from scapy.layers.inet import *
from scapy.all import *
import time
conf.L3socket=L3RawSocket
host_ip = '127.1.1.1'

openp = []
filterdp = []
dest_ports = [i for i in range(22000,25000)]
def is_up(ip):
    icmp = IP(dst=ip)/ICMP()
    resp = sr1(icmp, timeout=1)
    if resp == None:
        return False
    else:
        return True

def check_port(ip, port, result = 1):
    src_port = RandShort()
    try:
        p = IP(dst=ip)/TCP(sport=src_port, dport=port, flags='F')
        resp = sr1(p, timeout=0.5) # Sending packet
        if str(type(resp)) == "<type 'NoneType'>":
            result = 1
        elif resp.haslayer(TCP):
            if resp.getlayer(TCP).flags == 0x14:
                result = 0
            #icmp is blocked
            elif (int(resp.getlayer(ICMP).type)==3 and int(resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                result = 2
    except Exception as e:
        pass
    return result

def fin_main(dst):
  conf.verb = 0
  openp=[]
  dest_ports=[dst.split(":")[1]]
  host_ip=dst.split(":")[0]
  for port in dest_ports:
      response = check_port(host_ip, port)
      if response == 1:
          openp.append(port)
      elif response == 2:
          filterdp.append(port)
  if len(openp) != 0:
      print ("Possible Open or Filtered Ports:")
      print (openp)
  if len(filterdp) != 0:
      print ("Possible Filtered Ports:")
      print (filterdp)
  if (len(openp) == 0) and (len(filterdp) == 0):
          print ("No ports open")
  return openp

