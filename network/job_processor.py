from flask import Flask, request
import requests

app = Flask(__name__)

name_of_container = "name_of_container"  # should be id of docker container

@app.route('/', methods=['POST', 'GET'])
def give_job():
    # job_json = request.get_json(force=True)
    # ip_port = job_json['ip_port']
    # created_by = name_of_container
    # report_id = job_json['report_id']
    # scan_type = job_json['scan_type']
    return 'Received job!'


def send_job_result():
    result = {
            "ip_port": "127.0.0.1:36",
            "status": "Alive",
            "created_by": "Container 1",
            "report_id": 5
        }
    record_endpoint_of_django_server = 'http://127.0.0.1:8000/sb/records/'
    res = requests.post(record_endpoint_of_django_server, json=result)
    print("send job")

send_job_result()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')