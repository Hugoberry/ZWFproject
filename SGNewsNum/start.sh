#!/bin/bash
COUNTER=0
while [ $COUNTER -lt 300 ]
do
    python main.py
    sleep 10
done