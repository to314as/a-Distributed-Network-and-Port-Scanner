import asyncio
import requests
import sys
import logging
from flask import Flask, request
import sys
sys.path.insert(1, '/scanner_modules')
import scanner_tcp_socket
import scanner_tcp
import scanner_fin
import scanner_syn

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

job_queue = asyncio.Queue()

if len(sys.argv) <= 1:
    name_of_container = 'default_container_name_1'
else:
    name_of_container = sys.argv[1]

@app.route('/', methods=['POST'])
def give_job():
    file = open("/mnt/testfile.txt", "a+")
    file.write(f' Recived at node {name_of_container} ')
    file.close()
    job_json = request.get_json(force=True)
    ip_port = job_json['ip_port']
    created_by = name_of_container
    report_id = job_json['report_id']
    scan_type = job_json['scan_type']
    if scan_type=='TCP SYN':
      open_ports=scanner_fin.main(ip_port)
    elif scan_type=='TCP FIN':
      open_ports=scanner_fin.main(ip_port)
    elif scan_type=='FULL TCP CONNECT':
      open_ports=scanner_tcp.main(ip_port)
    else:
      open_ports=scanner_tcp.main(ip_port)
    file = open("/mnt/testfile.txt", "a+")
    file.write(" open: "+str(open_ports))
    file.close()
    send_job_result(open_ports)
    print(f'{ip_port} {report_id} {scan_type} {created_by}')
    return 'Received job!'

@app.route('/', methods=['GET'])
def home():
    return 'Started'

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
