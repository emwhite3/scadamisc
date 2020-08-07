#be able to push to all clients asking for sens val that is not present on this instance
#be able to recieve things

import socket
from socket import gethostbyname
import sys
import os
from datetime import datetime
import select
import Queue
import random

#tag = id
class Sensor:
    def __init__(self, tag):
        self.tag = tag
        self.value = 0
    
    def get_val(self):
        return str(random.randint(0,100))
        
def shutdown_sockets(inputs, outputs, exceptionally, messages_queue):
    print("DO SHUTDOWN SOCKETS")

def check_purge(hourly_record):
    if now.hour > hourly_record["hour"]:
        print("purging all sensor values....")
        for key in hourly_record:
            del hourly_record[key]
            hourly_record[key] = []
        hourly_record["hour"] = now.hour

def ask_slave_devices(outputs):
    return 0


now = datetime.now()

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

# Bind socket to port
hostName = gethostbyname('0.0.0.0')
port = 5004
server_address = (hostName, port)
print('starting up on %s port %s' % server_address)
server.bind(server_address)
# Listen for incoming connections
server.listen(5)

#Sockets on which to read and write from
inputs = [server] #putting stuff into
outputs = []      #outputting to

#outgoing message queue
message_queue = {}

#dictionary to store all sensor values
sens_list = {}
hourly_record = {"hour" : now.hour}

while inputs:
    #print("Waiting for network event....")
    #readable - incoming data available to read
    #writable - sockets free space to be written to
    #exceptional - sockets that have an error
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
    
    for socket in readable:
        if socket is server:
            connection, client_address = socket.accept()
            print("New connection from %s", client_address)
            connection.setblocking(0)
            inputs.append(connection)
            
            message_queue[connection] = Queue.Queue()
        else:
            sens_id = socket.recv(1024)
            if sens_id:
                if sens_id == 'kill':
                    print("shutting down connection, sensors, and server....")
                    subprocess.call("sudo shutdown now", shell=True)
                
                print("Recieved %s, getting value..." % sens_id)
                if sens_id not in sens_list:
                    ask_slave_devices()
                    #sens_list[sens_id] = Sensor(sens_id)
                print("sending value for %s" % sens_id)
                curr_val = sens_list[sens_id].get_val()
                message_queue[socket].put(curr_val)
                
                if sens_id not in hourly_record:
                    hourly_record[sens_id] = []
                hourly_record[sens_id].append(curr_val)
                
                check_purge(hourly_record)
                
                if socket not in outputs:
                    outputs.append(socket)
                #else:
                    #print("Closing %s, no new data...")
                    
                    #if socket in outputs:
                        #outputs.remove(socket)
                    #inputs.remove(socket)
                    #socket.close()
                    
                    #del message_queue[socket]
                    
    for socket in writable:
        try:
            out_message = message_queue[socket].get_nowait()
            print("sending message!")
        except Queue.Empty:
            continue
            #print("output queue for %s is empty" % socket)
            #outputs.remove(socket)
        else:
            socket.send(out_message)
    
    for socket in exceptional:
        print("handling exception on %s" %socket)
        inputs.remove(socket)
        if socket in outputs:
            outputs.remove(socket)
        socket.close()
        
        del message_queue[socket]

            