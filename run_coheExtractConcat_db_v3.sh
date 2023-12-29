#!/bin/bash

# コマンドライン引数をチェック
if [ $# -ne 7 ]; then
    echo "エラー: 7つの引数が必要です (sensor_name1, sensor_name2, dir1_axis, dir2_axis, nperseg, threshold1, threshold2 )"
    exit 1
fi

# 引数から変数を設定
sensor_name1=$1
sensor_name2=$2
dir1_axis=$3
dir2_axis=$4
nperseg=$5
threshold1=$6
threshold2=$7


# trainsディレクトリ内のサブディレクトリ一覧を取得
#trains_dir="/2021/v2158218/analyTrainData/trains/"
trains_dir="/gdsfs/gdsfs/mukai/jr/analyTrainData/trains/"
sub_dirs=("$trains_dir"*/)

# 処理を行う関数
process_directories() {
    local dir="$1"

    # 対応するディレクトリ名を生成
    local target_dir1="$dir$sensor_name1/"
    local target_dir2="$dir$sensor_name2/"
    
    # 信号1と信号2のファイル処理
    read first_file second_file <<< $(process_files "$target_dir1" "$dir1_axis")
    read third_file fourth_file <<< $(process_files "$target_dir2" "$dir2_axis")

    # Pythonスクリプトにファイルを渡す
    python3 ./readbinary_coherence_nperseg_extract_concat_db_v2.py "$first_file" "$second_file" "$third_file" "$fourth_file" "$nperseg" "$threshold1" "$threshold2"
    echo "$first_file"
}
# ファイル処理関数
process_files() {
    local target_dir="$1"
    local axis="$2"
    local file_array=($(ls "$target_dir"*_"$axis".bin | sort))
    local num_files=${#file_array[@]}

    if [[ $num_files -ne 1 && $num_files -ne 2 ]]; then
	echo "エラー: '${target_dir}' には1または2つのファイルが必要です。現在のファイル数: ${num_files}"
	exit 1
    fi

    if [[ $num_files -eq 1 ]]; then
	echo "${file_array[0]} none"
    else
	echo "${file_array[0]} ${file_array[1]}"
    fi
}

# 各ディレクトリに対して処理を行う
for dir in "${sub_dirs[@]}"; do
    process_directories "$dir"
done

