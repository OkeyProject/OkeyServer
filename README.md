# OkeyServer
# HOST 140.113.235.151
# Port 7975

Init:  
Send:
{
"command":  "game",
"setting": {
"log": "verbose" | "separate"
}
}
Receive
{
"status" : 0 | 1 ,
"message" : ""
}

Get Card In Hand:
Send
{
"player" : 1 | 2 | 3 | 4,
"action" : "hand"
}
Receive
{
"status": 0 | 1,
"cards" : [
{
"color" : "black" | "yellow" | "blue" | "red" | "empty",
"number" : 1~13
}, *24
]
}
Take Card:
Send:
{
"player": 1 | 2 | 3 | 4,
"action" : "take",
"from" : "deck" | "discard"
}
Receive
{
"status" : 0 | 1,
"card" : {
"color" : "black" | "yellow" | "blue" | "red",
"number" : 1~13
}
}
Throw Card:
Send:
{
"player": 1 | 2 | 3 | 4,
"action" : "throw",
"cards" : [
{
"empty" : 0 | 1 ,
"color" : "black" | "yellow" | "blue" | "red",
"number" : 1~13
} * 24
]
}
Receive:
{
"status" : 0 | 1,
"message" : ""
}
