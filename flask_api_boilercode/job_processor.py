import asyncio
import requests
import sys
import logging
from flask import Flask, request
import sys
sys.path.insert(1, '/scanner_modules')
import scanner_tcp_socket

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


def send_job_result(open_ports):
    result = {
            "ip_port": "127.0.0.1",
            "status": "Alive",
            "created_by": name_of_container,
            "open_ports": open_ports
        }
    record_endpoint_of_django_server = 'http://127.0.0.1:8000/sb/records/'
    res = requests.post(record_endpoint_of_django_server, json=result)
    print("send job")

async def worker(name, queue):
    while True:
        # Get a "work item" out of the queue.
        job = await queue.get()
        open_ports = scanner_tcp_socket.main()
        if not queue.empty():
          send_job_result(job[0])
        # Notify the queue that the "work item" has been processed.
        queue.task_done()

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
