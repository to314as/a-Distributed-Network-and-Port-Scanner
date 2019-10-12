import argparse
import scapy
import random
from scapy.all import sniff,Ether, ARP, srp, IP, UDP, raw, hexdump, sendp, Packet, XByteField, X3BytesField, DNS, ShortEnumField, ShortField, XShortField,bind_layers
from scapy.data import UDP_SERVICES

##aasignment3###
parser = argparse.ArgumentParser(description='Argumetns for receiver program',add_help=False)
parser.add_argument('-i', type=str, default='lo', help='the interface of the network card')
parser.add_argument('-p', type=int, default=9999, help='the port of the receiver')
parser.add_argument('-r', default=0.1, type=float, help='the probability of a wrong ACK or of a not reply at all')
args = parser.parse_args()

#define pur custom UDP package
class UDP(Packet):
    name = "UDP"
    fields_desc = [ ShortEnumField("sport", 53, UDP_SERVICES), #standard UDP
                    ShortEnumField("dport", 53, UDP_SERVICES),
                    ShortField("len", None),
                    XShortField("chksum", None), 
                    XByteField("ack",255), #Acknowlegment number - 8bit
                    X3BytesField("pkg",1)] #pakcage number -24 bit 
bind_layers(IP, UDP)   
 
def receive_pkg():
    x=sniff(iface=args.i, prn=send_ack,lfilter=lambda p: any(proto in p and (p[proto].dport in [args.p]) for proto in [UDP]))
    #filtering in scrappy is horrible. If this version does not work for your OS, try: filter = 'udp port '+str(args.p)+')')
    return

#define response once a message on the correct port is recived (send acknoweldgment to let the sender now about succesfull transmission)
def send_ack(pkt):
    rn=random.random()
    rn2=random.random()
    print('Receiving packet '+str(pkt[UDP].pkg))
    if rn>(args.r):
        print('Sending ACK '+str(pkt[UDP].pkg))
        packet = IP(dst=pkt[IP].src, src=pkt[IP].dst)/UDP(dport=pkt[UDP].sport,ack=255,pkg=pkt[UDP].pkg)
        sendp(Ether()/packet, iface=args.i,verbose=False)
    elif(rn2<=0.5):
        #force wrong acknowledgment
        print('Sending ACK 0')
        packet = IP(dst=pkt[IP].src, src=pkt[IP].dst)/UDP(dport=pkt[UDP].sport,ack=127,pkg=pkt[UDP].pkg)
        sendp(Ether()/packet, iface=args.i,verbose=False)
    else:
        #force timeout by no return
        print('Timeout')
    return
    
        
#receive_pkg()
x=sniff(iface=args.i, prn=send_ack,lfilter=lambda p: any(proto in p and (p[proto].sport in [args.p] or p[proto].dport in [args.p]) for proto in [UDP]))