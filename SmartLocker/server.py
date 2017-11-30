# Message Receiver
# Requires netifaces

import netifaces as ni
import os
from socket import *

OUTPUT_FILE = 'output.txt'

host = ""
port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)

ip = ni.ifaddresses('en1')[2][0]['addr']
print "IP is " + ip

print "Waiting to receive messages..."
while True:
    (data, addr) = UDPSock.recvfrom(buf)
    print "Received message: " + data
    out = open(OUTPUT_FILE, 'a')
    out.write(data + '\n')
    out.close()
    if data == "exit":
        break
UDPSock.close()
os._exit(0)