#!/bin/bash

python3 readbinary_peakVal_writecsv_v2.py ../tagTrains/ 1e+6 2>./log/peakVal_all_1e+6.error.log &
python3 readbinary_peakVal_writecsv_v2.py ../tagTrains/ 1e+7 2>./log/peakVal_all_1e+7.error.log &
python3 readbinary_peakVal_writecsv_v2.py ../tagTrains/ 1e+8 2>./log/peakVal_all_1e+8.error.log &
python3 readbinary_peakVal_writecsv_v2.py ../tagTrains/ 1e+9 2>./log/peakVal_all_1e+9.error.log &
python3 readbinary_peakVal_writecsv_v2.py ../tagTrains/ 1e+10 2>./log/peakVal_all_1e+10.error.log &
python3 readbinary_peakVal_writecsv_v2.py ../tagTrains/ 1e+11 2>./log/peakVal_all_1e+11.error.log &
python3 readbinary_peakVal_writecsv_v2.py ../tagTrains/ 1e+12 2>./log/peakVal_all_1e+12.error.log &

