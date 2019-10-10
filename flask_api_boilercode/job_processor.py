import asyncio
import requests
import sys
import logging

from flask import Flask, request

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

job_queue = asyncio.Queue()

if len(sys.argv) <= 1:
    name_of_container = 'default_container_name'
else:
    name_of_container = sys.argv[1]


@app.route('/', methods=['POST'])
def give_job():
    job_json = request.get_json(force=True)
    if job_json is None:
        logging.error('Faulty job receieved')
    else:
        ip_port = job_json['ip_port']
        scan_type = job_json['scan_type']
        report_id = job_json['report_id']
        job_queue.put((ip_port, scan_type, report_id))
        # get from queue if you wanna process a job
    return 'Received job!'


def send_job_result():
    result = {
            "ip_port": "127.0.0.1",
            "status": "Alive",
            "created_by": name_of_container,
            "report_id": 2
        }
    # record_endpoint_of_django_server = 'http://127.0.0.1:8000/sb/records/'
    # res = requests.post(record_endpoint_of_django_server, json=result)
    print("send job")

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
