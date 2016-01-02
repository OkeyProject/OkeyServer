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

def msgEncoder(msgtype, msg):
    recvmsg = {msgtype:msg}
    return json.dumps(recvmsg)

def menu(s, addr):
    gameState = False
    while True:
        recvdata = s.recv(2048)
        data = json.loads(recvdata)
        if 'command' not in data:
            s.sendall(msgEncoder('error','unknown '+str(data)))
        else:
            if data['command'] == "New":
                if not gameState:
                    gameState = True
                    s.sendall(msgEncoder('message','New Game Started. Please choose game mode [quiet,verbose,playerOnly]'))
                else:
                    s.sendall(msgEncoder('error','Game exists. Please use command \'Exit\' first if you want to change game mode'))
            elif data['command'] == "Exit":
                gameState = False
                s.sendall(msgEncoder('message','Game exit'))
            elif data['command'] == "Close":
                s.sendall(msgEncoder('message','Good Bye!'))
                break
            else:
                s.sendall(msgEncoder('error','unknown '+str(data)))

while True:
    connection, address = s.accept()
    thread.start_new_thread(menu,(connection,address))
