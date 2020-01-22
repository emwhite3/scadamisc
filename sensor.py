from time import gmtime, strftime
import random
import time
from network import Network

class Sensor:
    #The senor ID is set alongside an array that stores first thousand values
    #with its corresponding date and time
    def __init__(self, ident, host_ip, port):
        self.ident = ident
        self.zero = 0
        self.val = [['', 0] for i in range(1000)]
        self.net = Network(host_ip, port)
    
    def set_ident(self, ident):
        self.ident = ident
    
    #for now it reads from a text value, but in reality it should
    #pull a value from tthhe hardware sensor
    def get_curr_val(self):
        file = open("sensor.txt", "r+")
        for i in range(random.randint(1, 45)):
            file.readline()
        return int(file.readline())
    
    def get_curr_time(self):
        return strftime("%Y-%m-%d %H:%M:%S", gmtime())

    def update_val(self):
        if self.zero >= 1000:
            self.val = [['', 0] for i in range(1000)]
        self.val[self.zero] = [self.get_curr_time(), self.get_curr_val()]
        self.zero += 1
    
    def get_recent_val(self):
        if self.zero == 0:
            return self.val[0]
        return self.val[self.zero-1]
    
    #this will work to continuously push updated values to the host
    def cont_update(self):
        #while True:
        self.update_val()
        print(self.ident)
        self.net.push(self.ident, self.get_recent_val()[1], self.get_recent_val()[0])
        print(self.get_recent_val())
        time.sleep(1)
        
        


