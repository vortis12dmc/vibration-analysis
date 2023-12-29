#!/bin/bash

# コマンドライン引数をチェック
if [ $# -ne 6 ]; then
    echo "エラー: 引数の数が不正です．"
    echo "使用方法: $0 <ディレクトリ名> <軸> <ディレクトリ名> <軸> <nperseg> <閾値>"
    exit 1
fi

# ファイル処理関数
process_files() {
    local target_dir=$1
    local axis=$2
    local file_array=($(ls "$target_dir"*_"$axis".bin | sort))
    local num_files=${#file_array[@]}

    if [[ num_files -ne 1 && num_files -ne 2 ]]; then
        echo "エラー: '$target_dir' には1または2つのファイルが必要です。"
        exit 1
    fi

    if [[ num_files -eq 1 ]]; then
        echo "${file_array[0]} none"
    else
        echo "${file_array[0]} ${file_array[1]}"
    fi
}

# 引数からディレクトリ名と軸を取得
target_dir1=$1
dir1_axis=$2
target_dir2=$3
dir2_axis=$4
nperseg=$5
threshold=$6

# 信号1と信号2のファイル処理
read first_file second_file <<< $(process_files "$target_dir1" "$dir1_axis")
read third_file fourth_file <<< $(process_files "$target_dir2" "$dir2_axis")

# Pythonスクリプトにファイルを渡す
python3 ./readbinary_fft_extract_concat.py "$first_file" "$second_file" "$third_file" "$fourth_file" "$nperseg" "$threshold"

