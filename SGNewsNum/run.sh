#!/bin/bash
COUNTER=0
while [ $COUNTER -lt 300 ]
do
    cd e:
    cd ZWFpro/SGNewsNum/
    python main.py
    sleep 10
done