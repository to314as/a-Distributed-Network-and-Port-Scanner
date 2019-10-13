import asyncio
import requests
import argparse
import logging
import random
import time
from flask import Flask, request

logging.basicConfig(level=logging.DEBUG)
parser = argparse.ArgumentParser(description="Job processor")
parser.add_argument("-p", "--port", type=int, help="Port of receiver")
parser.add_argument("-i", "--reportid", type=int, help="Report ID")

args = parser.parse_args()

app = Flask(f'{__name__}_{args.port}')
job_queue = asyncio.Queue()

name_of_container = f'container_{args.port}'
running_scan_flag = False


def not_running_scan():
    global running_scan_flag
    running_scan_flag = False


def running_scan():
    global running_scan_flag
    running_scan_flag = True


def generate_random_result(rate):
    if random.random() < rate:
        return 'Alive'
    else:
        return 'Not Alive'


@app.route('/', methods=['POST'])
def give_job():
    job_json = request.get_json(force=True)
    ip_port = job_json['ip_port']
    created_by = name_of_container
    report_id = job_json['report_id']
    scan_type = job_json['scan_type']
    job_queue.put((ip_port, scan_type, report_id))
    result = {
        "ip_port": ip_port,
        "status": generate_random_result(0.8),
        "created_by": name_of_container,
        "report_id": args.reportid,
    }
    time.sleep(0.01)
    record_endpoint_of_django_server = 'http://127.0.0.1:8000/sb/records/'
    res = requests.post(record_endpoint_of_django_server, json=result)
    if not running_scan_flag:
        running_scan()
        # pop first item off queue and process it
    print(f'{ip_port} {report_id} {scan_type} {created_by}')
    return 'Received job!'


@app.route('/', methods=['GET'])
def home():
    return 'Started'


def send_job_result(ip_port, status):
    result = {
        "ip_port": ip_port,
        "status": status,
        "created_by": name_of_container,
        "report_id": args.reportid,
    }
    record_endpoint_of_django_server = 'http://127.0.0.1:8000/sb/records/'
    res = requests.post(record_endpoint_of_django_server, json=result)
    not_running_scan()
    if not job_queue.empty():
        running_scan()
        # pop first item of queue and process it
    print("send job")


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=args.port)
