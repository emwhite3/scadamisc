import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_address = ('192.168.4.8', 5000)

sock.connect(host_address)
print("Connected!")
