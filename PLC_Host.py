import socket
from socket import gethostbyname
import sys
import os

def get_val(sens):
	return str(50)



# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
hostName = gethostbyname('0.0.0.0')
port = 5004
server_address = (hostName, port)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print ('waiting for a connection')
    connection, client_address = sock.accept()
	try:
		print ('connection from %s', client_address)
		break


while True:
    try:
        sens = connection.recv(1024)
		print(sens)
        print('Getting value for %s' % sens)
		connection.sendall(get_val(sens))
	
	except KeyboardInterrupt:
		connection.close()
		os._exit(1)  
		    
    finally:
        # Clean up the connection
        connection.close()