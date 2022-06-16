import socketserver
import re
from dnsResolver import resolve
from mikrotikRemote import commandMikrotik
import configparser
from time import sleep



config = configparser.ConfigParser()
config.read('config.ini')
mikrotik_ip = config['mikrotik_info']['ip']
ssh_port = config['ssh_info']['port']
username = config['mikrotik_info']['username']
password = config['mikrotik_info']['password']

syslog_ip = config['syslog_info']['ip']
syslog_port = config['syslog_info']['port']

mikrotik_addresslist = config['mikrotik_config']['addresslist_name']

LOG_FILE = 'youlogfile.log'
HOST, PORT = syslog_ip, int(syslog_port)


class SyslogUDPHandler(socketserver.BaseRequestHandler):

	def handle(self):
		data = bytes.decode(self.request[0].strip())
		socket = self.request[1]
		filterd = re.findall(r".*done query.*10.10.34.35.*",str(data))
		if filterd != []:
			filterd = filterd[0]
			filterd = filterd.split(" ")
			domain = filterd[-2]
			print(domain)
			ips = resolve(domain)
			print(ips)
			for ip in ips:
				command = "ip dns static add address="+ip+" type=A name="+domain
				commandMikrotik(mikrotik_ip,ssh_port,username,password,command)
				sleep(2)
				command2 ="ip firewall address-list add address="+ip+" list="+mikrotik_addresslist
				commandMikrotik(mikrotik_ip,ssh_port,username,password,command2)
				sleep(2)


if __name__ == "__main__":
	while True:
		try:
			server = socketserver.UDPServer((HOST,PORT), SyslogUDPHandler)
			server.serve_forever(poll_interval=0.5)
		except (IOError, SystemExit) as e:
			print(e)
			print("An error happend , retry...")
			sleep(5)
			continue
		# 	raise
		# except KeyboardInterrupt:
		# 	print ("Crtl+C Pressed. Shutting down.")
