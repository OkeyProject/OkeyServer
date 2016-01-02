#!/bin/sh
ps auxww | grep cwlin | grep python | awk '{print $2}' | xargs kill -9
python2.7 /u/cs/102/0216053/OkeyServer/main.py &
