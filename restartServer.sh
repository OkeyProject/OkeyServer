#!/bin/sh
ps auxww | grep cwlin | grep python | grep -v grep | awk '{print $2}' | xargs kill -9
python2.7 /u/cs/102/0216053/OkeyServer/server.py & 
