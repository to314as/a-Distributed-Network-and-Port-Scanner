from scapy.all import RandShort,sr1,TCP,sr,IP,ICMP,UDP,L3RawSocket
import time

conf.L3socket=L3RawSocket #needed because things on lo with scapy can be very messy
dst_ip = '127.1.1.1'
src_port = RandShort()
dest_ports = [i for i in range(22000,22200)]

def is_up(ip):
    icmp = IP(dst=ip)/ICMP()
    resp = sr1(icmp, timeout=0.5,verbose=False)
    if resp == None:
        return False
    else:
        return True

def is_up_udp(ip):
    icmp = IP(dst=ip)/UDP(dport=0)
    resp = sr1(icmp, timeout=0.5,verbose=False)
    if resp == None:
        return False
    else:
        return True

def main(dst):
  file = open("/mnt/testfile.txt", "a+")
  file.write(str(dst))
  file.close()
  dst_ports=[dst.split(":")[1]]
  dst_ip=dst.split(":")[0]
  file = open("/mnt/testfile.txt", "a+")
  file.write(" d_p: "+str(dst_ports))
  file.close()
  open_ports=[]
  for port in dst_ports:
    file = open("/mnt/testfile.txt", "a+")
    file.write(" p: "+str(port))
    file.close()
    port=int(port)
    #establishe a tcp connection
    tcp_connect_scan_resp = sr1(IP(dst=dst_ip)/TCP(sport=src_port,dport=port,flags="S"),timeout=0.5,verbose=False)
    #check if the connection was accepted and returned a not non-type response
    if(str(type(tcp_connect_scan_resp))=="<class 'NoneType'>"):
      continue
      #print("Closed, filtered, dropped or blocked")
    elif(tcp_connect_scan_resp.haslayer(TCP)):
        #if it was accapted we should read the SYN-ACK in the flags. This will be 0x12 in hexadecimal as SYN(=2) and ACK(=16 or 0x10 in hex).
      if(tcp_connect_scan_resp.getlayer(TCP).flags == 0x12):
       send_rst = sr(IP(dst=dst_ip)/TCP(sport=src_port,dport=port,flags="AR"),timeout=0.5,verbose=False)
       open_ports.append(port) 
      #if we read 0x14 this implies RST-ACK, so the port is closed.
      elif (tcp_connect_scan_resp.getlayer(TCP).flags == 0x14):
          continue
    print(open_ports)
  else:
      print("Host is Down")
  file = open("/mnt/testfile.txt", "a+")
  file.write("_scannerend_")
  file.close()
  return open_ports
               
if __name__ == '__main__':
    start=time.time()
    open_ports=[]
    for dst_port in dest_ports:
      #establishe a tcp connection
      tcp_connect_scan_resp = sr1(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="S"),timeout=0.5,verbose=False)
      #check if the connection was accepted and returned a not non-type response
      if(str(type(tcp_connect_scan_resp))=="<class 'NoneType'>"):
        print("Closed, filtered, dropped or blocked")
      elif(tcp_connect_scan_resp.haslayer(TCP)):
          #if it was accapted we should read the SYN-ACK in the flags. This will be 0x12 in hexadecimal as SYN(=2) and ACK(=16 or 0x10 in hex).
        if(tcp_connect_scan_resp.getlayer(TCP).flags == 0x12):
         send_rst = sr(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="AR"),timeout=0.5,verbose=False)
         open_ports.append(dst_port)
         print("Open")
          #if we read 0x14 this implies RST-ACK, so the port is closed.
        elif (tcp_connect_scan_resp.getlayer(TCP).flags == 0x14):
          continue
          #print("Closed")
    print(open_ports)
    print(time.time()-start)