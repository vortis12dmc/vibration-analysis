#!/bin/bash

# ファイル処理関数
process_files() {
    local target_dir=$1
    declare -A file_pairs

    # ディレクトリ内のすべての .bin ファイルを処理
    for file in "$target_dir"*.bin; do
        # ファイル名から識別子を取得
        #local identifier=$(basename "$file" | cut -d'_' -f1-4)
        local identifier=$(basename "$file" | rev | cut -d'.' -f2 | cut -d'_' -f1 | rev)

        # ペアを作成
        if [[ -z ${file_pairs[$identifier]} ]]; then
            file_pairs[$identifier]="$file"
        else
            file_pairs[$identifier]+=" $file"
        fi
    done

    # ペアの出力
    for key in "${!file_pairs[@]}"; do
        local pair=(${file_pairs[$key]})
        if [[ ${#pair[@]} -eq 1 ]]; then
            echo "${pair[0]} none"
        else
            echo "${pair[@]}"
        fi
    done
}

# スタートディレクトリ（この例では特定のディレクトリを直接指定）
#START_DIR="../concatTrains/1004_S548_R06/A_In_Rail/"
# 特定のディレクトリのみを処理
#echo "Entering directory: $START_DIR"

#threshold=30

    # ディレクトリ内のファイルペアを処理
#while read first_file second_file; do
#    echo "Processing files: $first_file and $second_file"
    # ファイルに対して操作を行う
    # 例: Pythonスクリプトにファイルを渡す
#    python3 ./readbinary_fft_extract_concat.py "$first_file" "$second_file" "$threshold"
#done < <(process_files "$START_DIR")

# 列車名のリスト
train_names=(
    "0418_K000"
    "1004_S548_R06"
    "1504_S560_R02"
    "1920_T332_U01"
    "0608_S540_S19"
    "1020_T312_U01"
    "1520_T322_U03"
    "1938_S572_R05"
    "0630_T300_U06"
    "1039_S550_R05"
    "1542_S562_R08"
    "1956_T334_U03"
    "0701_S400_U01"
    "1116_M606_R03"
    "1550_T324_U07"
    "2035_M614_S08"
    "0707_T302_R08"
    "1120_T314_U08"
    "1604_S564_S18"
    "2038_T336_U06"
    "0719_M600_R10"
    "1142_S552_S08"
    "1620_T326_U06"
    "2111_S406_S02"
    "0727_T304_U09"
    "1150_U5960A_S13"
    "1642_S566_S11"
    "2156_T338_S03"
    "0742_S542_S15"
    "1211_U3960A_R07"
    "1704_S568_S19"
    "2234_T340_R03"
    "0745_T306_U03"
    "1220_T316_U09"
    "1720_T328_U09"
    "2317_S408_S16"
    "0806_T308_U08"
    "1242_S554_S03"
    "1747_M608_S15"
    "0819_M602_S17"
    "1317_S402_S07"
    "1804_S570_S01"
    "0839_S544_S01"
    "1320_T318_U06"
    "1820_T330_U07"
    "0916_M604_S02"
    "1342_S556_S16"
    "1840_M610_R01"
    "0920_T310_U07"
    "1420_T320_U08"
    "1902_S404_U08"
    "0939_S546_S05"
    "1442_S558_R04"
    "1913_M612_S05"
)


# センサ名のリスト
sensor_names=(
    "A_In_Rail"
    "A_Out_Bond"
    "A_Out_Rail"
    "B_In_Rail"
    "B_Out_Bond"
    "B_Out_Rail"
)


threshold=30

# 列車名のリストをループ
for train in "${train_names[@]}"; do
    # センサ名のリストをループ
    for sensor in "${sensor_names[@]}"; do
        # ディレクトリを設定
        START_DIR="../concatTrains/$train/$sensor/"

        # 特定のディレクトリのみを処理
        echo "Entering directory: $START_DIR"

        # ディレクトリ内のファイルペアを処理
        while read first_file second_file; do
            echo "Processing files: $first_file and $second_file"
            # ファイルに対して操作を行う
            python3 ./readbinary_fft_extract_concat.py "$first_file" "$second_file" "$threshold"
        done < <(process_files "$START_DIR")
    done
done
