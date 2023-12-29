# ファイルパスを定義します。実際のファイルパスに置き換えてください。
file_path = 'check_binaryfile_num.txt' # ここに実際のファイルパスを入力してください。

# ファイルを開いて読み込みます。
with open(file_path, 'r') as file:
    lines = file.readlines()

# 行をソートします。
sorted_lines = sorted(lines)

# ソートされた行を表示します。
for line in sorted_lines:
    print(line.strip())

