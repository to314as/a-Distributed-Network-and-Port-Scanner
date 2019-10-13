import os
import requests
import subprocess
#
# client = docker.from_env()
# container = client.containers.run(image='n', ports={'5000/tcp': ('127.0.0.1', 5000)},
#                                   command='python job_processor.py container_1 &', detach=True)
# for container in client.containers.list():
#     print(container.logs())

job = {
    'ip_port': '127.0.0.1:999',
    'scan_type': 'Is-Alive',
    'report_id': '4',
}
job_endpoint_of_flask_scanningnode = f'http://127.0.0.2:5000'  # depends on container
res = requests.post(job_endpoint_of_flask_scanningnode, json=job)
#
# for container in client.containers.list():
#     container.stop()
#     print(container.log)
