import os

import docker
import requests
import subprocess

# create docker images
absolute_dirpath = os.path.abspath(os.path.dirname(__file__))
os.chdir(os.path.join(absolute_dirpath, "victim"))

# create the attacker nodes
os.chdir(os.path.join(absolute_dirpath, "network"))
# os.chdir('/home/tobias/networkscanner/network')  # adjust to your path
os.system('docker build -t n .')
os.system(f'docker run -d --network host --cap-add=NET_ADMIN --name n3 n  python job_processor.py n3 &')
# result = subprocess.run(['docker', 'inspect', '-f', '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}', ], stdout=subprocess.PIPE)
#
# print('result')
# print(result.stdout)
# print('end result')
# #
# # client = docker.from_env()
# # container = client.containers.run(image='n', ports={'5000/tcp': ('127.0.0.1', 5000)},
# #                                   command='python job_processor.py container_1 &', detach=True)
# # for container in client.containers.list():
# #     print(container.logs())
#
job = {
    'ip_port': '127.0.0.1:999',
    'scan_type': 'Is-Alive',
    'report_id': '4',
}
job_endpoint_of_flask_scanningnode = f'http://172.17.0.2:5000'  # depends on container
res = requests.post(job_endpoint_of_flask_scanningnode, json=job)
print(res)
os.system("docker stop $(docker ps -a -q")
os.system("docker rm $(docker ps -a -q")
# #
# # for container in client.containers.list():
# #     container.stop()
# #     print(container.log)
