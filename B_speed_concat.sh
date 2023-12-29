#!/bin/bash

# トップレベルのディレクトリに対してループ
for dir in ../trains/*; do
    # B_In_Railディレクトリが存在するか確認
    if [[ -d "$dir/B_In_Rail" ]]; then
        # B_In_Railディレクトリ内の全ての'_z.bin'で終わるファイルを時間順にソート
        files=($(ls "$dir/B_In_Rail/"*_z.bin | sort))

        # 配列の要素数を取得
        num_files=${#files[@]}

        # ファイルが1つしかない場合は、"$second_file"に"nothing"を渡す
        if [[ num_files -eq 1 ]]; then
            first_file=${files[0]}
            second_file="nothing"
            python3 ./readbinary_speedCalc_trainSet_concat.py "$first_file" "$second_file" 500 >> ../output/B_Speed.txt 2>>../output/B_Speed.error.log
            continue # 次のディレクトリに移動
        fi

        # 2つのファイルを順番に処理するループ
        for (( i=0; i<$((num_files-1)); i++ )); do
            # 最初のファイルを取得
            first_file=${files[i]}
            # 次のファイルを取得
            second_file=${files[i+1]}

            # Pythonスクリプトに2つのファイルを渡す
            python3 ./readbinary_speedCalc_trainSet_concat.py "$first_file" "$second_file" 500 >> ../output/B_Speed.txt 2>>../output/B_Speed.error.log
        done
    fi
done
