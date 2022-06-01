import paramiko
from base64 import decodebytes

def commandMikrotik(ip,port,username,password,command):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,port=port, username=username, password=password)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)