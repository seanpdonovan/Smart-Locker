import datetime
import os
import sys
from subprocess import call
from socket import *
import time

# set the default ip as what my computer is
host = "123.456.7.890"

# can pass another server ip when calling this program
if len(sys.argv) == 2:
    host = sys.argv[1]

port = 13000
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)

# contains list of authorized users
USER_FILE = "users.txt"

# keeps the local copy of the output log
OUTPUT_FILE = "output.txt"

# time the lock stays unlocked before relocking
RELOCK_DELAY = 10

# UH ID cards are "%1234567;"
def parseInput(InString):
    newString = InString[1:8] + " " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return newString

# check if authorized
def isApproved(User):
    approved = False
    if User in open(USER_FILE).read():
        approved = True
    return approved

Input = ""
while Input != "exit":
    Input = raw_input()
    if Input != "":
        if Input == "exit":    # type exit to close client and server
            UDPSock.sendto(Input, addr)
            UDPSock.close()
            exit()
        Input = parseInput(Input)    # convert to usable string from card add date/time
        if isApproved(Input[:7]):    # check user ID
            UDPSock.sendto(Input, addr)    # send ID and date/time to server
            out = open(OUTPUT_FILE, 'a')    # write to local log
            out.write(Input + '\n')
            out.close()
            call(["sh", "unlock.sh"])    # unlock the lock
            time.sleep(RELOCK_DELAY)
            call(["sh", "lock.sh"])    # relock the lock
        elif isApproved(Input[:7]) == False:
            AD = "Access Denied for: " + Input
            UDPSock.sendto(AD, addr)    # send Access Denied message to server
            out = open(OUTPUT_FILE, 'a')    # write Access Denied message to local log
            out.write(AD + '\n')
            out.close()
    print(Input)
