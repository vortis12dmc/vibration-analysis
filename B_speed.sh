#!/bin/bash

for i in ../trains/*/B_In_Rail/*z.bin; do
    python3 ./readbinary_speedCalc_trainSet.py "$i" 500 >> ../output/B_speed.txt 2>> ../output/B_speed.log.error
done

