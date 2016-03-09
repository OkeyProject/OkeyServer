#!/bin/sh
ps auxww | grep python | grep -v grep | awk '{print $2}' | xargs kill -9
python2.7 /home/Justin/OkeyServer/server.py &
