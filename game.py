from random import shuffle
import json
import socket
import collections

def Err(msg):
    print(str(msg)+"\n")
    return json.dumps({"status": 0, "message": msg})

def IsStraight(group):
    group.sort(key=lambda x: x[1])
    cmpVal = group[0][1]
    for i in group:
        if i[1] != cmpVal:
            return False
        cmpVal = cmpVal + 1
    return True

def IsKind(group):
    colors = collections.Counter(group)
    result =colors.most_common(24)
    for i in result:
        if int(i[1]) != 1:
            return False
    cmpVal = group[0][1]
    for i in group:
        if i[1] != cmpVal:
            return False
    return True

def GroupChk(group):
    if len(group) < 3:
        return False
    if IsStraight(group) or IsKind(group):
        return True
    else:
        return False

def WinChk(hand):
    start = -1
    end = 0
    for i in range(0,len(hand)):
        if hand[i][0] != "empty" and start < end:
            start = i
        elif hand[i][0] != "empty" and start >= end:
            end = i + 1
            if not GroupChk(hand[start:end]):
                return False
    return True

def getHand(s,hand,deck):
    msg = {"status": 1,"cards":{"hand":[{"color":i[0],"number":i[1]} for i in hand],"deck":{"all":{},"top":{}}}}
    for j in range(1,5):
        msg['cards']['deck']['all'].update({"player"+str(j):[]})
        msg['cards']['deck']['top'].update({"player"+str(j):{}})
    for i in range(1,5):
        msg['cards']['deck']['all']['player'+str(i)] = [{"color":j[0],"number":j[1]} for j in deck[int(i)-1]]
        if len(deck[int(i)-1]) > 0:
            msg['cards']['deck']['top']['player'+str(i)] = {"color":deck[int(i)-1][-1:][0],"number":deck[int(i)-1][-1:][1]}

    print(msg)
    s.sendall(json.dumps(msg))

def ThrowCard(data, turn, player, curDrawed):
    if not "cards" in data:
        return False, "Parse cards error",[],False
    if len(data['cards']) != 24:
        return False, "Cards amount error",[],False
    newHand = [(i['color'],i['number']) for i in data['cards']]
    oldHand = player[turn] + [curDrawed]
    newCmp = collections.Counter(newHand)
    oldCmp = collections.Counter(oldHand)
    oldCmp.subtract(newCmp)
    result = oldCmp.most_common(24)
    resultCount = 0
    thrownCard = []
    for i in result:
        if int(i[1]) < 0 or int(i[1]) > 1:
            return False,"Do not cheat",[],False
        elif int(i[1]) == 1 and resultCount == 0:
            thrownCard = i[0]
            resultCount = resultCount + 1
    if resultCount != 1:
        return False,"Do not cheat",[],False
    else:
        if WinChk([(i[0],i[1]) for i in data['cards']]):
            return True,json.dumps({"status": 1,"message":"You Win !!","Win":1}),thrownCard,True
        else:
            return True,json.dumps({"status": 1,"message":"Complete!","Win":0}),thrownCard,False

def TakeCard(data, turn ,cardStack, discard):
    if not "from" in data:
        return False, "Where to take card?",[]
    if data['from'] != "deck" and data['from'] != "discard":
        return False, "Wrong place",[]
    if data['from'] == "deck":
        if len(cardStack) == 0:
            return False, "Deck is already empty",[]
        newcard = cardStack.pop()
        return True, json.dumps({"status": 1,"card":{"color":newcard[0],"number":newcard[1]}}), newcard
    elif data['from'] == "discard":
        if turn == 0:
            LastPlayer = 3
        else:
            LastPlayer = turn - 1
        if len(discard[LastPlayer]) == 0:
            return False,"No cards there",[]
        newcard = discard[LastPlayer].pop()
        return True, json.dumps({"status": 1,"card":{"color":newcard[0],"number":newcard[1]}}),newcard

def RecvDataChk(data,turn):
    if not "player" in data:
        return False,"data error"
    if int(data['player']) < 1 or int(data['player']) > 4:
        return False,"Player number fault"
    if int(data['player']) != turn + 1:
        return False, "Not this player's round"
    if not "action" in data:
        return False, "No action specified"
    return True, ""


def Game(s,logType):
    colors = ["blue","yellow","red","black"]
    cardStack = [(i,j) for i in colors for j in range(1,14)] * 2
    shuffle(cardStack)
    shuffle(cardStack)

    player = []
    discard = [ [],[],[],[] ]
    for i in range(0,4):
        player.append([cardStack.pop() for j in range(0,14)])
        for j in range(0,10):
            player[i].append(("empty",-1))

    turn = 0
    while True:
        gameState = 0
        curDrawed = []
        isWin = False
        while True:
            try:
                data = json.loads(s.recv(2048))
            except ValueError:
                print("JSON decode failed")

            errState,errMsg = RecvDataChk(data,turn)

            if not errState:
                s.sendall(Err(errMsg))
                continue

            if data['action'] == "hand":
                getHand(s,player[turn],discard)
            elif data['action'] == "take":
                if gameState != 0:
                    s.sendall(Err("You've take the card already"))
                    continue
                takeState, takeMsg, curDrawed = TakeCard(data, turn, cardStack, discard)
                if takeState:
                    print("take: "+str(curDrawed))
                    gameState = 1
                    s.sendall(takeMsg)
                else:
                    s.sendall(Err(takeMsg))
            elif data['action'] == "throw":
                if gameState != 1:
                    s.sendall(Err("Please take before you throw"))
                    continue
                throwState,throwMsg,thrownCard,isWin = ThrowCard(data, turn, player,curDrawed)
                if throwState:
                    print("throw: "+str(thrownCard))
                    discard[turn].append(thrownCard)
                    s.sendall(throwMsg)
                    gameState = 0
                    break
                else:
                    s.sendall(Err(throwMsg))

        if isWin:
            s.close()
            break

        if turn == 3:
            turn = 0
        else:
            turn = turn + 1

