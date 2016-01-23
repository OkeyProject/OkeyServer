#!/usr/bin/env python2.7

import socket
import json
import thread

HOST = "140.113.235.151"
PORT = 7975

address = (HOST,PORT)

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(address)
s.listen(10)

def Err(msg):
    retmsg = {"status": 0, "message": msg}
    return json.dumps(retmsg)

def recvDataDecoder(data):
    return json.loads(data)

def main(s, addr):
    data = recvDataDecoder(s.recv(2048))
    if data['command'] == "game":
        if "setting" in data and "log" in data['setting']:
            if data['setting']['log'] != "verbose" or data['setting']['log'] != "separate":
                s.sendall(Err("Unknown log type"))
            else:
                print("Game Start")
        else:
            s.sendall(Err("Setting Error"))


while True:
    connection, address = s.accept()
    thread.start_new_thread(main,(connection,address))
