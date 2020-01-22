import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("169.254.165.142", 5000)
sock.bind(server_address)

sock.listen(1)

while True:
    print("waiting for connection")
    connection, client_address = sock.accept()

    try:
        print("connection from %s", client_address)
        
        while True:
            data = connection.recv(1024)
            print("recieved %s", data)
            if data:
                connection.sendall(data)
            else:
                break
    finally:
        connection.close()