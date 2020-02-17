import socket
import sys
import Queue
from socket import gethostbyname
from subprocess import call
from pathlib import Path

#create host socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostName = gethostbyname('0.0.0.0')
port = 5004
server_address = (hostName, port)
server.bind(server_address)
server.listen(10)

inputs = [server] #putting stuff into
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
            sens_id = socket.recv(1024)
            if sens_id:
                
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

            