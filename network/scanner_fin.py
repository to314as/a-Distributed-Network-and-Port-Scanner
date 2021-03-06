from scapy.all import IP,sr1,ICMP,TCP,RandShort,L3RawSocket
import time
conf.L3socket=L3RawSocket #needed because things on lo with scapy can be very messy
host_ip = '127.1.1.1'

openp = []
filterdp = []
dest_ports = [i for i in range(22200,22300)]
def is_up(ip):
    icmp = IP(dst=ip)/ICMP()
    resp = sr1(icmp, timeout=1)
    if resp == None:
        return False
    else:
        return True

def check_port(ip, port, result = 0):
    src_port = RandShort()
    try:
        p = IP(dst=ip)/TCP(sport=src_port, dport=port, flags='F')
        resp = sr1(p, timeout=2) # Sending packet
        #print(resp)
        if resp == None:
            result = 1
            return result
        elif resp.haslayer(TCP):
            if resp.getlayer(TCP).flags == 0x14:
                result = 0
            #icmp is blocked
            elif (int(resp.getlayer(ICMP).type)==3 and int(resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                result = 2
    except Exception as e:
        pass
    return result
    
def main(dst):
  conf.verb = 0 
  openp=[]
  dest_ports=[dst.split(":")[1]]
  host_ip=dst.split(":")[0]
  for port in dest_ports:
      response = check_port(host_ip, int(port))
      if response == 1:
          openp.append(port)
      elif response == 2:
          filterdp.append(port)
  return openp
       
        
if __name__ == '__main__':
    conf.verb = 0 
    start=time.time()
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
    print(time.time()-start)


