from scapy.all import RandShort,sr1,TCP,sr,IP,ICMP,UDP,L3RawSocket
conf.L3socket=L3RawSocket
dst_ip = '127.0.0.2'
src_port = RandShort()
dst_port=9998

def is_up(ip):
    icmp = IP(dst=ip)/ICMP()
    resp = sr1(icmp, timeout=1,verbose=False)
    print(resp)
    if resp == None:
        return False
    else:
        return True

def is_up_udp(ip):
    icmp = IP(dst=ip)/UDP(dport=0)
    resp = sr1(icmp, timeout=1,verbose=False)
    print(resp)
    if resp == None:
        return False
    else:
        return True

        
if __name__ == '__main__':
    open_ports=[]
    if is_up(dst_ip):
        for dst_port in range(1000,10000):
          #establishe a tcp connection
          tcp_connect_scan_resp = sr1(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="S"),timeout=0.5,verbose=False)
          #check if the connection was accepted and returned a not non-type response
          if(str(type(tcp_connect_scan_resp))=="<class 'NoneType'>"):
            continue
            #print("Closed, filtered, dropped or blocked")
          elif(tcp_connect_scan_resp.haslayer(TCP)):
              #if it was accapted we should read the SYN-ACK in the flags. This will be 0x12 in hexadecimal as SYN(=2) and ACK(=16 or 0x10 in hex).
            if(tcp_connect_scan_resp.getlayer(TCP).flags == 0x12):
             send_rst = sr(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="AR"),timeout=0.5,verbose=False)
             open_ports.append(dst_port)
                #print("Open")
              #if we read 0x14 this implies RST-ACK, so the port is closed.
            elif (tcp_connect_scan_resp.getlayer(TCP).flags == 0x14):
                continue
                #print("Closed")
        print(open_ports)
    else:
        print("Host is Down")