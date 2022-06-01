
# import imp
# import logging
import socketserver
# import time
import re
from dnsResolver import resolve
from mikrotikRemote import commandMikrotik
import configparser

LOG_FILE = 'youlogfile.log'
HOST, PORT = "0.0.0.0", 514

config = configparser.ConfigParser()
config.read('config.ini')
mikrotik_ip = config['mikrotik_info']['ip']
ssh_port = config['mikrotik_info']['ssh_port']
username = config['mikrotik_info']['username']
password = config['mikrotik_info']['password']


# logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='', filename=LOG_FILE, filemode='a')

class SyslogUDPHandler(socketserver.BaseRequestHandler):

	def handle(self):
		data = bytes.decode(self.request[0].strip())
		socket = self.request[1]
		# files = open('weblog.txt', 'a')
		filterd = re.findall(r".*done query.*10.10.34.35.*",str(data))
		if filterd != []:
			filterd = filterd[0]
			filterd = filterd.split(" ")
			domain = filterd[-2]
			ips = resolve(domain)
			for ip in ips:
				command = "ip dns static add address="+ip+" type=A name="+domain
				commandMikrotik(mikrotik_ip,ssh_port,username,password,command)
				command2 ="ip firewall address-list add address="+ip+" list=zzzBypassFilter"
				commandMikrotik(mikrotik_ip,ssh_port,username,password,command2)
			# files.write(str(filterd) + "\n")
			# files.close()


if __name__ == "__main__":
	try:
		server = socketserver.UDPServer((HOST,PORT), SyslogUDPHandler)
		server.serve_forever(poll_interval=0.5)
	except (IOError, SystemExit):
		raise
	except KeyboardInterrupt:
		print ("Crtl+C Pressed. Shutting down.")
