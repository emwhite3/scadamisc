import socket
import sys
from subprocess import call
from pathlib import Path

file_name = "master_config.json"
json_file = Path(file_dir)

#check if file exists, if it does then we delete the file
if json_file.is_file():
    subprocess.call("rm %s", %file_name, shell=True)

#create file to be written to from network
subprocess.call("touch %s", file_name, shell=True)

#create a client and connect to host

sock = socket.socket()
sock.connect('192.168.4.0', 5010)
file = open(file_name, 'wb')

#read data from host and write to file
while True:
    data = sock.recv(1024)
    while data:
        file.write(data)
        data = sock.recv(1024)

#clean all running processes
file.close()
socket.close()