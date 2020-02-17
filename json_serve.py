import socket
import sys
import Queue
import select
from socket import gethostbyname
from subprocess import call
from pathlib import Path

#https://stackoverflow.com/questions/9382045/send-a-file-through-sockets-in-python
#https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions

def get_file():
    file = open("master_config.json", "rb")
    return file

def queue_json(message_queue, socket):
    file = get_file()
    #read file in chunks, in this case it is  read in 1024 b or 1 kb
    data = file.read(1024)
    while data:
        message_queue[socket].put(data)
        data = file.read(1024)
    return

def get_host():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostName = gethostbyname('0.0.0.0')
    port = 5004
    server_address = (hostName, port)
    server.bind(server_address)
    server.listen(10)
    print("started json server on %s", server_address)
    return server


inputs = [get_host()] #putting stuff into
outputs = []      #outputting to
message_queue = {}


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
            queue_json(message_queue, socket)
    for socket in writable:
        try:
            out_message = message_queue[socket].get_nowait()
            print("sending message!")
        except Queue.Empty:
            #                                                                                                                         continue
            print("output queue for %s is empty" % socket)
            outputs.remove(socket)
        else:
            print("."),
            socket.send(out_message)
    
    for socket in exceptional:
        print("handling exception on %s" %socket)
        inputs.remove(socket)
        if socket in outputs:
            outputs.remove(socket)
        socket.close()
        
        del message_queue[socket]

            