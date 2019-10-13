import asyncio
import requests
import argparse
import logging
import random
import queue
from flask import Flask, request
# from starboardscanner_app import *

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


# def get_status(ip_port, scan_type):
#     if scan_type == 'TCP SYN':
#         open_ports = scanner_syn.main(ip_port)
#     elif scan_type == 'TCP FIN':
#         open_ports = scanner_fin.main(ip_port)
#     elif scan_type == 'FULL TCP CONNECT':
#         open_ports = scanner_tcp.main(ip_port)
#     else:
#         open_ports = scanner_tcp.is_up(ip_port)
#     if len(open_ports) == 0:
#         return 'Down'
#     else:
#         return 'Up'


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


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=args.port)
