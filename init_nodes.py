import os
import random
import numpy as np

amount_of_nodes = 5
existing_ports = 65535
amount_of_ports = 5
file = open("testfile2.txt", "w")
file.write("start ")
file.close()

# create docker images
absolute_dirpath = os.path.abspath(os.path.dirname(__file__))
os.chdir(os.path.join(absolute_dirpath, "victim"))
# os.chdir('/home/tobias/networkscanner/victim')  # adjust to your path
#os.system('docker build -t v .')


# a function to define a random subset of open ports on the victim machine
def open_ports(n):
  open_ports=''
  ports=[]
  for i in range(0,n):
    p=int(random.random()*existing_ports)
    ports.append(p)
    open_ports+=f'-p 127.1.1.1:{p}:{p} '
  ports=np.array(ports)
  np.save('victim_ports', ports)
  return open_ports, ports

#create the victim server with a given number of open ports
open_ports_string=open_ports(amount_of_ports)[0]
open_ports=open_ports(amount_of_ports)[1]
print(open_ports)
#os.system(f'docker run '+open_ports_string+f' --name victim --cap-add=NET_ADMIN --network="scanner" v python3 setup_server.py {open_ports} &')

# create the attacker nodes
os.chdir(os.path.join(absolute_dirpath, "network"))
# os.chdir('/home/tobias/networkscanner/network')  # adjust to your path
os.system('docker build -t n .')

for i in range(amount_of_nodes):
            os.system(f'docker run -p 5000{i}:5000 --network="host"  --name container_{i} --cap-add=NET_ADMIN -u root -v /home/tobias/networkscanner:/mnt n sudo python job_processor.py container_{i} &')
            #--network="scanner" --ip 172.0.0.{i}
