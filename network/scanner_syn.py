from scapy.all import IP,sr1,ICMP,TCP,RandShort,sr,L3RawSocket
import time
conf.L3socket=L3RawSocket
host_ip = '127.0.0.1'

openp = []
filterdp = []
dest_ports = [i for i in range(22000,25000)]
def is_up(ip):
    icmp = IP(dst=ip)/ICMP()
    resp = sr1(icmp, timeout=10)
    if resp == None:
        return False
    else:
        return True

def main(dst):
  dest_ports=[dst.split(":")[1]]
  host_ip=dst.split(":")[0]
  openp=[]
  if is_up(host_ip):
      for port in dest_ports:
          #print (port)
          response = check_port(host_ip, port)
          if response == 1:
              openp.append(port)

      if len(openp) != 0:
          print ("Open Ports:")
          print (openp)
      else:
          print ("No ports open")

      if len(filterdp) != 0:
          print ("Possible Filtered Ports:")
          print (filterdp)
      return openp
  else:
      print ("Host is Down")
  return openp
        
def check_port(ip, port, result = 1):
    src_port = RandShort()
    try:
        p = IP(dst=ip)/TCP(sport=src_port, dport=port, flags='S')
        resp = sr1(p, timeout=2) # Sending packet
        if str(type(resp)) == "<type 'NoneType'>":
            result = 0
        elif resp.haslayer(TCP):
            if resp.getlayer(TCP).flags == 0x12:
                send_rst = sr(IP(dst=ip)/TCP(sport=src_port, dport=port, flags='AR'), timeout=0.5)
                result = 1
            elif resp.getlayer(TCP).flags == 0x14:
                result = 0
            #icmp is blocked
            elif (int(resp.getlayer(ICMP).type)==3 and int(resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                result = 2
    except Exception as e:
        pass

    return result


if __name__ == '__main__':
    conf.verb = 0 
    start=time.time()
    for port in dest_ports:
        #print (port)
        response = check_port(host_ip, port)
        if response == 1:
            openp.append(port)

    if len(openp) != 0:
        print ("Open Ports:")
        print (openp)
    else:
        print ("No ports open")

    if len(filterdp) != 0:
        print ("Possible Filtered Ports:")
        print (filterdp)
    print(time.time()-start)


