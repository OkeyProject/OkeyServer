from random import shuffle
def Game(s,logType):
    colors = ["blue","yellow","red","black"]
    cardStack = [(i,j) for i in colors for j in range(1,14)] * 2
    shuffle(cardStack)
    shuffle(cardStack)

    player = []
    for i in range(0,4):
        player.append([cardStack.pop() for j in range(0,14)])

    while True:
        s.recv(2048)

