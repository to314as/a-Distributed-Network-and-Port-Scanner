#remove running dockers
import os
amount_of_nodes=5

#os.system('docker stop victim')
#os.system('docker rm victim')
for i in range(amount_of_nodes):
    os.system(f'docker stop container_{i}')
    os.system(f'docker rm container_{i}')