import socket
import sys
from sensor import Sensor

host_ip = "192.168.4.9"
port = 5000
sens01 = Sensor("Sensor 001", host_ip, port)
sens01.cont_update()


