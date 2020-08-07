#ADD ip address enter in python launch
#Add a way to connect to hosting s

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

def read_sens():
    file = open("sens_list.txt", "r+")
    sens = []
    for line in file:
        sens.append(line)
    return sens

#read text file then populate list with sensor objects
def get_sens_list(socket):
    sens = read_sens()
    for ident in sens:
        sens_list[ident] = Sensor(ident)
        print("sending value for %s" % sens_id)
        curr_val = sens_list[ident].get_val()
        message_queue[socket].put(curr_val)
        
        if sens_id not in hourly_record:
            hourly_record[sens_id] = []
        hourly_record[sens_id].append(curr_val)
        
        if socket not in outputs:
            outputs.append(socket)

now = datetime.now()

# In thhis case we are connecting to the host
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.4.10'
port = 5004
host_address = (host_ip, port)
s.connect(host_address)

#connect to host then add to input            
message_queue[s] = Queue.Queue()

#Sockets on which to read and write from
inputs = [s] #putting stuff into
outputs = []      #outputting to

#outgoing message queue
message_queue = {}

#dictionary to store all sensor values
sens_list = get_sens_list()
hourly_record = {"hour" : now.hour}

while inputs:
    print("Waiting for network event....")
    #readable - incoming data available to read
    #writable - sockets free space to be written to
    #exceptional - sockets that have an error
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
    
    for socket in readable:
    
        sens_id = socket.recv(1024)
        if sens_id:
            if sens_id == 'kill':
                print("shutting down connection, sensors, and s....")
                subprocess.call("sudo shutdown now", shell=True)
            
            print("Recieved %s, getting value..." % sens_id)
            message_queue[socket].put(get_sens_value(sens_id))
                    
    for socket in writable:
        try:
            out_message = message_queue[socket].get_nowait()
        except Queue.Empty:
            print("output queue for %s is empty" % socket)
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



