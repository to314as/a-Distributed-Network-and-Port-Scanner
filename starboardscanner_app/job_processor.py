import asyncio
import requests
import argparse
import logging
import random
import queue
from flask import Flask, request
from scapy.layers.inet import *
from scapy.all import *

# import sys
# sys.path.append("../Shares/templates")

logging.basicConfig(level=logging.DEBUG)
parser = argparse.ArgumentParser(description="Job processor")
parser.add_argument("-p", "--port", type=int, help="Port of receiver")
parser.add_argument("-i", "--reportid", type=int, help="Report ID")

args = parser.parse_args()

app = Flask(f'{__name__}_{args.port}')
job_queue = queue.Queue()

name_of_container = f'container_{args.port}'
running_scan_flag = False


def running_scan():
    global running_scan_flag
    running_scan_flag = True


def not_running_scan():
    global running_scan_flag
    running_scan_flag = False


def generate_random_result(rate):
    if random.random() < rate:
        return 'Up'
    else:
        return 'Down'


def get_status(ip_port, scan_type):
    if scan_type == 'TCP SYN':
        open_ports = tcp_main(ip_port)
    elif scan_type == 'TCP FIN':
        open_ports = fin_main(ip_port)
    elif scan_type == 'FULL TCP CONNECT':
        open_ports = syn_main(ip_port)
    else:
        open_ports = is_up(ip_port)
    if len(open_ports) == 0:
        return 'Down'
    else:
        return 'Up'


@app.route('/', methods=['POST'])
def give_job():
    print(f'running scan flag {running_scan_flag}')
    job_json = request.get_json(force=True)
    ip_port = job_json['ip_port']
    created_by = name_of_container
    report_id = job_json['report_id']
    scan_type = job_json['scan_type']
    job_queue.put((ip_port, scan_type, report_id))
    print('put in job queue')
    print(f'running scan flag {running_scan_flag}')
    if not running_scan_flag:
        running_scan()
        (ip_port, scan_type, report_id) = job_queue.get()
        # send_job_result(ip_port, get_status(ip_port, scan_type))
        print('calling send job result')
        send_job_result(ip_port, generate_random_result(0.8), report_id)
    print(f'{ip_port} {report_id} {scan_type} {created_by}')
    return 'Received job!'


@app.route('/', methods=['GET'])
def home():
    return 'Started'


def send_job_result(ip_port, status, report_id):
    result = {
        "ip_port": ip_port,
        "status": status,
        "created_by": name_of_container,
        "report_id": report_id,
    }
    record_endpoint_of_django_server = 'http://127.0.0.1:8000/sb/records/'
    res = requests.post(record_endpoint_of_django_server, json=result)
    not_running_scan()
    if not job_queue.empty():
        running_scan()
        (ip_port, scan_type, report_id) = job_queue.get()
        # send_job_result(ip_port, get_status(ip_port, scan_type))
        send_job_result(ip_port, generate_random_result(0.8))
    print("send job")


conf.L3socket = L3RawSocket
host_ip = '127.1.1.1'

openp = []
filterdp = []
dest_ports = [i for i in range(22000, 25000)]


def is_up(ip):
    icmp = IP(dst=ip) / ICMP()
    resp = sr1(icmp, timeout=1)
    if resp == None:
        return False
    else:
        return True


def check_port(ip, port, result=1):
    src_port = RandShort()
    try:
        p = IP(dst=ip) / TCP(sport=src_port, dport=port, flags='F')
        resp = sr1(p, timeout=0.5)  # Sending packet
        if str(type(resp)) == "<type 'NoneType'>":
            result = 1
        elif resp.haslayer(TCP):
            if resp.getlayer(TCP).flags == 0x14:
                result = 0
            # icmp is blocked
            elif (int(resp.getlayer(ICMP).type) == 3 and int(resp.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]):
                result = 2
    except Exception as e:
        pass
    return result


def fin_main(dst):
    conf.verb = 0
    openp = []
    dest_ports = [dst.split(":")[1]]
    host_ip = dst.split(":")[0]
    for port in dest_ports:
        response = check_port(host_ip, port)
        if response == 1:
            openp.append(port)
        elif response == 2:
            filterdp.append(port)
    if len(openp) != 0:
        print("Possible Open or Filtered Ports:")
        print(openp)
    if len(filterdp) != 0:
        print("Possible Filtered Ports:")
        print(filterdp)
    if (len(openp) == 0) and (len(filterdp) == 0):
        print("No ports open")
    return openp


conf.L3socket = L3RawSocket
dst_ip = '127.0.0.2'
src_port = RandShort()
dst_ports = [i for i in range(20000, 65535)]


def is_up(ip):
    icmp = IP(dst=ip) / ICMP()
    resp = sr1(icmp, timeout=1, verbose=False)
    print(resp)
    if resp == None:
        return False
    else:
        return True


def is_up_udp(ip):
    icmp = IP(dst=ip) / UDP(dport=0)
    resp = sr1(icmp, timeout=1, verbose=False)
    print(resp)
    if resp == None:
        return False
    else:
        return True


def tcp_main(dst):
    open_ports = []
    for port in dst_ports:
        port = int(port)
        # establishe a tcp connection
        tcp_connect_scan_resp = sr1(IP(dst=dst_ip) / TCP(sport=src_port, dport=port, flags="S"), timeout=0.5,
                                    verbose=False)
        # check if the connection was accepted and returned a not non-type response
        if (str(type(tcp_connect_scan_resp)) == "<class 'NoneType'>"):
            continue
            # print("Closed, filtered, dropped or blocked")
        elif (tcp_connect_scan_resp.haslayer(TCP)):
            # if it was accapted we should read the SYN-ACK in the flags. This will be 0x12 in hexadecimal as SYN(=2) and ACK(=16 or 0x10 in hex).
            if (tcp_connect_scan_resp.getlayer(TCP).flags == 0x12):
                send_rst = sr(IP(dst=dst_ip) / TCP(sport=src_port, dport=port, flags="AR"), timeout=0.5, verbose=False)
                open_ports.append(port)
            # if we read 0x14 this implies RST-ACK, so the port is closed.
            elif (tcp_connect_scan_resp.getlayer(TCP).flags == 0x14):
                continue
        print(open_ports)
    else:
        print("Host is Down")
    return open_ports

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

def syn_main(dst):
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
