#nohup ./run_coheExtractConcat_db_v4.sh A_Out_Bond A_Out_Rail y y 4096 50 400 2>log/A_Out_Bond-Rail_y-y.error.log &
#nohup ./run_coheExtractConcat_db_v4.sh A_Out_Bond B_Out_Bond y y 4096 50 50 2>log/A_Out_Bond-B_Out_Bond_y-y.error.log &
#nohup ./run_coheExtractConcat_db_v4.sh B_Out_Bond B_Out_Rail y y 4096 50 400 2>log/A_Out_Bond-B_Out_Bond_y-y.error.log &

#nohup ./run_coheExtractConcat_db_v4.sh B_In_Rail B_Out_Rail y y 4096 200 200 2>log/B_In-Out_Rail_y-y.error.log &
#nohup ./run_coheExtractConcat_db_v4.sh A_In_Rail A_Out_Rail y y 4096 200 200 2>log/A_In-Out_Rail_y-y.error.log &
#nohup ./run_coheExtractConcat_db_v4.sh A_Out_Rail B_Out_Rail y y 4096 200 200 2>log/A-B_Out_Rail_y-y.error.log &

nohup ./run_coheExtractConcat_db_v4.sh A_Out_Bond A_Out_Rail y z 4096 50 400 2>log/A_Out_Bond-Rail_y-z.error.log &
nohup ./run_coheExtractConcat_db_v4.sh B_Out_Bond B_Out_Rail y z 4096 50 400 2>log/B_Out_Bond-Rail_y-z.error.log &
