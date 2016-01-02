#!/usr/bin/env python2.7

import socket
import json

HOST = "140.113.235.151"
PORT = 7975

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

address = (HOST,PORT)

s.connect(address)

while True:
    msgtype = raw_input("type>")
    if msgtype == "exitClient":
        break
    msg = raw_input("msg>")
    jsonmsg = {msgtype:msg}
    s.sendall(json.dumps(jsonmsg))
    data = s.recv(2048)
    print(data)
