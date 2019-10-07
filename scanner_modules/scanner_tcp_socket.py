import socket,sys,os

os.system('clear')

host_ip = '127.0.0.1'

open_ports =[]
start_port = 0
end_port = 1000

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

for p in range(start_port, end_port+1):
	sys.stdout.flush()
	response = probe_port(host_ip, p)
	if response == 0:
		open_ports.append(p)
	if not p == end_port:
		sys.stdout.write('\b' * len(str(p)))
	
if open_ports:
	print("Open Ports")
	print(sorted(open_ports))
else:
	print("No ports open")

