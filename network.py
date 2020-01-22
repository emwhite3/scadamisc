import socket
import sys

class Network:
    def __init__(self, host_ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_address = (host_ip, port)
        print(self.host_address)
        self.verify()
        
    def verify(self):
        try:
            print("connecting")
            self.sock.connect(self.host_address)
            print("Successfully connected to host!")
            print(self.host_address)
        except:
            print("Unsuccessful Connection to host!")
            print(self.host_address)
            sys.exit()
        
    def push(self, ident, val, time):
        data = "%s, %d, %s" % (ident, val, time)
        print("Sending message %s" % data)
        self.sock.sendall(data)
        #delivered = False
        #while !delivered:
        
