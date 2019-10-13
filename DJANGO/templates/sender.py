import argparse
import scapy
from scapy.all import sniff, Ether, ARP, srp, IP, UDP, raw, hexdump, sendp, Packet, XByteField, X3BytesField, DNS, \
    ShortEnumField, ShortField, XShortField, AsyncSniffer, bind_layers
from scapy.data import UDP_SERVICES

##aasignment3###
parser = argparse.ArgumentParser(description='Argumetns for sender program', add_help=False)
parser.add_argument('-h', type=str, default='127.0.0.1', help='the IP address of the receiver')
parser.add_argument('-i', type=str, default='lo', help='the interface of the network card')
parser.add_argument('-p', type=int, default=9999, help='the port of the receiver')
# value in seconds
parser.add_argument('-t', default=1, type=int, help='the timeout of the sender in seconds')
# n must be lower than 256 as in our architecture it is stored within 8 bits.
parser.add_argument('-n', default=5, type=int,
                    help=' the number of packets that the sender will send. In case the server does not receive an ACK from the receiver should re-send the same packet. This counts as one packet')
args = parser.parse_args()


# function only needed for closer inspection of packages /testing purposes
def expand(x):
    yield x.name
    while x.payload:
        x = x.payload
        yield x.name


# define pur custom UDP package
class UDP(Packet):
    name = "UDP"
    fields_desc = [ShortEnumField("sport", 53, UDP_SERVICES),  # standard UDP
                   ShortEnumField("dport", 53, UDP_SERVICES),
                   ShortField("len", None),
                   XShortField("chksum", None),
                   XByteField("ack", 0),  # Acknowlegment number - 8bit
                   X3BytesField("pkg", 1)]  # pakcage number -24 bit


bind_layers(IP, UDP)
lastn = 1


# create and send out a pkg
def create_pkg(n):
    packet = IP(dst=args.h, src=args.h, ttl=args.t) / UDP(sport=args.p - 1, dport=args.p, ack=0, pkg=n)
    packet = IP(raw(packet))
    # print(list(expand(packet))) if we want to have a look inside the layers of the package
    print('Sending packet ' + str(packet[UDP].pkg))
    sendp(Ether() / packet, iface=args.i, verbose=False)
    a_s = sniff(iface=args.i, prn=ack,
                lfilter=lambda p: any(proto in p and (p[proto].dport in [args.p - 1]) for proto in [UDP]),
                timeout=args.t, stop_filter=lambda x: x.haslayer(UDP))
    return


# check if the send message was recived correctly by comparing recived to expected acknowledgment
def ack(pkt):
    global lastn
    if (pkt[UDP].ack == 255 and pkt[UDP].pkg == lastn):
        print("Packet " + str(pkt[UDP].pkg) + " send and delivered succesfully")
        lastn += 1
        return
    elif (lastn <= args.n):
        print("Wrong acknowledgment, sending again")
        create_pkg(lastn)
    return


# make sure to succesuflly send n(as given by the user) packages
while lastn <= args.n:
    # a_s=AsyncSniffer(iface=args.i, prn=ack,lfilter=lambda p: any(proto in p and (p[proto].dport in [args.p-1]) for proto in [UDP]),timeout=args.t)
    # a_s.start()
    k = lastn
    create_pkg(lastn)
    # if no package was send pack inform the user over the timeout
    if (k == lastn):
        print('Timeout')
