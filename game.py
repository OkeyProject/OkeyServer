from random import shuffle
import json
import socket

def Err(msg):
    return json.dumps({"status": 0, "message": msg})

def getHand(s,hand):
    msg = {"status": 1,"cards":[{"color":i[0],"number":i[1]} for i in hand]}
    s.sendall(json.dumps(msg))




def Game(s,logType):
    colors = ["blue","yellow","red","black"]
    cardStack = [(i,j) for i in colors for j in range(1,14)] * 2
    shuffle(cardStack)
    shuffle(cardStack)

    player = []
    for i in range(0,4):
        player.append([cardStack.pop() for j in range(0,14)])
        for j in range(0,10):
            player[i].append(("empty",-1))

    turn = 0
    while True:
        while True:
            data = json.dumps(s.recv(2048))
            if "player" in data and data['player'] >=1 and data['player'] <=4:
                if data['player'] == turn+1:
                    if "action" in data:
                        if data['action'] == "hand":
                            getHand(s,player[turn])
                    else:
                        s.sendall(Err("No action specified"))
                else:
                    s.sendall(Err("Not this player's round"))
            else:
                s.sendall(Err("Player def error"))



        if turn == 3:
            turn = 0
        else:
            turn = turn + 1

