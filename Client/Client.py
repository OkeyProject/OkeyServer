#!/usr/bin/env python2.7

import sys
import socket
import json
import getopt
import subprocess


HOST = "140.113.235.151"
PORT = 7975

address = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    opts, args = getopt.getopt(sys.argv[1:], "p:c:vs", "")
except getopt.GetoptError:
    print("Opt Error")

aiList = []
logMode = "verbose"

for opt,arg in opts:
    if opt == "-p":
        aiList.append(("python", arg))
    elif opt == "-c":
        aiList.append(("c", arg))
    elif opt == "-v":
        logMode = "verbose"
    elif opt == "-s":
        logMode = "separate"
    else:
        print("unknown")

turn = 1

sock.connect(address)

if len(aiList) <= 0:
    print("No Ai Script Specified.")
    exit()

initObj = {}
initObj['command'] = "game"
initObj['setting'] = {"player": len(aiList), "log" : logMode}
sock.sendall(json.dumps(initObj))

while True:



    if turn == len(aiList):
        turn = 1
    else:
        turn = turn + 1


