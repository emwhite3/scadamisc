import socket
import sys
import os
import time
import select
import random

#tag = id
Class sensor():
    def __init__(self, tag):
        self.tag = tag
        self.value = 0
    
    def get_val(self):
        return str(random.randint(0,100))
        

def recieve_sens(sock):
    #waits x seconds for timeout
    
    ready = select.select([sock], [], [], 120)
    if ready[0]:
        return sock.recv(1024)
        
    

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

#object reference
sens_list = []
hourly_record = []



while True:
    # Wait for a connection
    print ('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print ('connection from %s', client_address)
        break
    except:
        print("Something!")

#We set blocking to zero
#sock.setblocking(0)
while True:
    try:
        sens = recieve_sens(sock)
        #print(sens)
        print('Getting value for %s' % sens)
        connection.sendall(get_val(sens))
    
    except KeyboardInterrupt:
        connection.close()
        os._exit(1)  
            