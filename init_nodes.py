import os
import random
amount_of_nodes=2
existing_ports=65535
amount_of_ports=5

#create docker images
os.chdir('/home/tobias/networkscanner/victim')
os.system('docker build -t v .')
os.chdir('/home/tobias/network')
os.system('docker build -t n .')

#a function to define a random subset of open ports on the victim machine
def open_ports(n):
  open_ports=''
  for i in range(0,n):
    p=random.randint(1,existing_ports)
    open_ports+=f'-p {p}:{p} '
  print(open_ports)
  return open_ports
 
#create the victim server with a given number of open ports
open_ports=open_ports(amount_of_ports) 
os.system(f'docker run '+open_ports+' --name victim v python')

#create the attacker nodes
for i in range(amount_of_nodes):
            os.system(f'docker run -p {5000 + i}:5000 --name n{i} n python job_processor.py container_{i} &')
            