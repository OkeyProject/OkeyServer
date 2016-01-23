#!/usr/bin/env python2.7

import socket
import json

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.connect(("140.113.235.151",7975))

data = {"command":"game","setting":{"log":"verbose"}}

sock.sendall(json.dumps(data))

print(sock.recv(2048))


