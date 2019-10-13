import socket,sys,os
import time

os.system('clear')

host_ip = '127.1.1.1'

open_ports =[]
dest_ports = [i for i in range(20000,60000)]

def probe_port(host, port, result = 1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        r = sock.connect_ex((host, port))
        if r == 0:
            result = r
        sock.close()
    except Exception as e:
        pass

    return result
 
def main(dst):
    dest_ports=[dst.split(":")[1]]
    host_ip=dst.split(":")[0]
    for p in dest_ports:
        sys.stdout.flush() #don't store things in the buffer put if there are "news" write them immediatly
        response = probe_port(host_ip,p)
        if response == 0:
          open_ports.append(p)
        if not p == end_port:
          sys.stdout.write('\b' * len(str(p)))
    
    if open_ports:
        print("Open Ports")
        print(sorted(open_ports))
    else:
        print("No ports open")
    return sorted(open_ports)
    
if __name__ == '__main__':    
    start=time.time()
    for p in dest_ports:
        sys.stdout.flush() #don't store things in the buffer put if there are "news" write them immediatly
        response = probe_port(host_ip, p)
        if response == 0:
            open_ports.append(p)
        
    if open_ports:
        print("Open Ports")
        print(sorted(open_ports))
    else:
        print("No ports open")#
    print(time.time()-start)

