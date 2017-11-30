import datetime
import os
from socket import *

#set host to the IP of the server computer
host = "192.168.1.113"
port = 13000
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)

USER_FILE = "users.txt"
OUTPUT_FILE = "output.txt"

def parseInput(InString):
    newString = InString[1:8] + " " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return newString

def isApproved(User):
    approved = False
    if User in open(USER_FILE).read():
        approved = True
    return approved

Input = "Beginning Program"
while Input != "exit":
    Input = raw_input()
    if Input != "":
        if Input == "exit":
            UDPSock.sendto(Input, addr)
            UDPSock.close()
            exit()
        Input = parseInput(Input)
        if isApproved(Input[:7]):
            UDPSock.sendto(Input, addr)
            out = open(OUTPUT_FILE, 'a')
            out.write(Input + '\n')
            out.close()
    print(Input)