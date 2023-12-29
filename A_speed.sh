#!/bin/bash

for i in ../trains/*/A_Out_Bond/*y.bin; do
    python3 ./readbinary_speedCalc_trainSet.py "$i" 100 >> ../output/A_speed.txt 2>> ../output/A_speed.log.error
done

