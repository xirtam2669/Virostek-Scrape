#!/bin/bash

for file in $(ls /home/xirtam/Documents/programs/Python/Scrape/Virostek-Scrape/apns/split-apns)
do
    screen python3 scrape-stable1.1.py $file
    wait 
done
