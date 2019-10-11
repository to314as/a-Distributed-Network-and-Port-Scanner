#remove running dockers
import os
amount_of_nodes=2

os.system('docker stop victim')
os.system('docker rm victim')
for i in range(amount_of_nodes):
    os.system(f'docker stop n{i}')
    os.system(f'docker rm n{i}')