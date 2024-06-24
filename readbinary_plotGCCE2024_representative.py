import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import coherence, csd
from scipy import signal
import struct

writeFilePass = "/gdsfs/gdsfs/mukai/jr/analyTrainData/output/GCCE2024_Plot/"

titleFontSize = 16
#titleLoc = 'center'
#titlex = 0

args = sys.argv
arguments_count = len(sys.argv)
if arguments_count < 13:
    print("Usage: "+args[0]+" <信号1の前半> <信号1の後半> <信号2の前半> <信号2の後半> <信号3の前半> <信号3の後半> <信号4の前半> <信号4の後半> ・・・ <信号6の後半>")
    sys.exit(1)

#num1 = []
#num2 = []

# num配列を定義
num = [[] for _ in range(6)]

readFile = [
    [args[1], args[2]],
    [args[3], args[4]],
    [args[5], args[6]],
    [args[7], args[8]],
    [args[9], args[10]],
    [args[11], args[12]]
]


#threshold_val = int(args[9])  #30  #信号部分の切り出し閾値

fs = 6400 #サンプリング周波数

# axis配列を定義する
axis = [
    readFile[0][0][-5].upper(),
    readFile[1][0][-5].upper(),
    readFile[2][0][-5].upper(),
    readFile[3][0][-5].upper(),
    readFile[4][0][-5].upper(),
    readFile[5][0][-5].upper()
]

split_readFile = [
    readFile[0][0].split('/'),
    readFile[1][0].split('/'),
    readFile[2][0].split('/'),
    readFile[3][0].split('/'),
    readFile[4][0].split('/'),
    readFile[5][0].split('/')
]

writeFile = writeFilePass + "_repData" + split_readFile[0][2] + ".eps"
writeFilePrev = writeFilePass + "_repData" + split_readFile[0][2] + ".png"

#sprit_readFile1 = readFile1.split('\\')
#sprit_readFile2 = readFile2.split('\\')

"""
accTitle = [
    "Raw " + split_readFile[0][2] + '/' + split_readFile[0][3] + '/' + axis[0] + "-axis",
    "Raw " + split_readFile[1][2] + '/' + split_readFile[1][3] + '/' + axis[1] + "-axis",
    "Raw " + split_readFile[2][2] + '/' + split_readFile[2][3] + '/' + axis[2] + "-axis",
    "Raw " + split_readFile[3][2] + '/' + split_readFile[3][3] + '/' + axis[3] + "-axis",
    "Raw " + split_readFile[4][2] + '/' + split_readFile[4][3] + '/' + axis[4] + "-axis",
    "Raw " + split_readFile[5][2] + '/' + split_readFile[5][3] + '/' + axis[5] + "-axis"
]
"""

# 置換操作を行う関数
def replace_strings(s):
    s = s.replace("A_", "N_")
    s = s.replace("B_", "F_")
    s = s.replace("In", "Left")
    s = s.replace("Out", "Right")
    return s

# 各文字列に対して置換操作を行う
sensorNameGCCE = [replace_strings(entry[3]) for entry in split_readFile]

"""
accTitle = [
    "Raw " + split_readFile[0][2] + '/N' + split_readFile[0][3][1:] + '/' + axis[0] + "-axis",
    "Raw " + split_readFile[1][2] + '/N' + split_readFile[1][3][1:] + '/' + axis[1] + "-axis",
    "Raw " + split_readFile[2][2] + '/N' + split_readFile[2][3][1:] + '/' + axis[2] + "-axis",
    "Raw " + split_readFile[3][2] + '/F' + split_readFile[3][3][1:] + '/' + axis[3] + "-axis",
    "Raw " + split_readFile[4][2] + '/F' + split_readFile[4][3][1:] + '/' + axis[4] + "-axis",
    "Raw " + split_readFile[5][2] + '/F' + split_readFile[5][3][1:] + '/' + axis[5] + "-axis"
]
"""

accTitle = [
    "Raw " + split_readFile[0][2] + '/' + sensorNameGCCE[0] + '/' + axis[0] + "-axis",
    "Raw " + split_readFile[1][2] + '/' + sensorNameGCCE[1] + '/' + axis[1] + "-axis",
    "Raw " + split_readFile[2][2] + '/' + sensorNameGCCE[2] + '/' + axis[2] + "-axis",
    "Raw " + split_readFile[3][2] + '/' + sensorNameGCCE[3] + '/' + axis[3] + "-axis",
    "Raw " + split_readFile[4][2] + '/' + sensorNameGCCE[4] + '/' + axis[4] + "-axis",
    "Raw " + split_readFile[5][2] + '/' + sensorNameGCCE[5] + '/' + axis[5] + "-axis"
]


# 各ファイルペアに対して処理を行う関数
def process_files(file_pair, num_list):
    with open(file_pair[0], 'rb') as f:
        data1 = f.read()
    for i in range(0, len(data1), 2):
        two_bytes = data1[i:i+2]
        (value,) = struct.unpack('<h', two_bytes)
        num_list.append(value)

    if file_pair[1] != "none":
        with open(file_pair[1], 'rb') as f:
            data2 = f.read()
        for i in range(0, len(data2), 2):
            two_bytes = data2[i:i+2]
            (value,) = struct.unpack('<h', two_bytes)
            num_list.append(value)

# すべてのファイルペアに対して処理を行う
for idx, file_pair in enumerate(readFile):
    process_files(file_pair, num[idx])

# 各データのデータ数を出力
for i, num_list in enumerate(num):
    data_count = len(num_list)
    print(f"The number of data{i + 1}: {data_count}")


# 処理後の信号データを格納するための配列
signal = [[] for _ in range(6)]

threshold_val=50; #仮

for i, num_list in enumerate(num):
    print(f"signal{i + 1} 処理前: {len(num_list)}")

    # 規定値以上の値が最初に出現するインデックスを検索
    start_index = next((i for i, x in enumerate(num_list) if x >= threshold_val), None)
    # 規定値以上の値が最後に出現するインデックスを検索
    end_index = len(num_list) - next((i for i, x in enumerate(reversed(num_list)) if x >= threshold_val), None)

    # 条件に合致する部分リストを抽出
    if start_index is not None and end_index is not None:
        signal[i] = np.array(num_list[start_index:end_index])

    print(f"signal{i + 1} 処理後: {len(signal[i])}")


"""
print("signal1 処理前: "+str(len(num1)))
# 処理：強い振動が起きている範囲の切り出し
# 規定値以上の値が最初に出現するインデックスを検索
start_index = next((i for i, x in enumerate(num1) if x >= threshold_val), None)
# 規定値以上の値が最後に出現するインデックスを検索
end_index = len(num1) - next((i for i, x in enumerate(reversed(num1)) if x >= threshold_val), None)
# 条件に合致する部分リストを抽出
signal1 = np.array(num1[start_index:end_index])

print("signal1 処理後: "+str(len(signal1)))
print("signal2 処理前: "+str(len(num2)))

# 同様の処理
start_index = next((i for i, x in enumerate(num2) if x >= threshold_val), None)
end_index = len(num2) - next((i for i, x in enumerate(reversed(num2)) if x >= threshold_val), None)
signal2 = np.array(num2[start_index:end_index])

print("signal2 処理後: "+str(len(signal2)))
"""

#fs_1 = (int)((data1_d_N)/(int(duration)*2))*2 #サンプリング周波数 (実際の値)
#dt=1/fs_1

print("Sampling frequency: " + str(fs))
#print("Sampling frequency: " + str(fs_1))
#print("Sampling frequency: " + str(fs_2))

# 時間配列を格納するための配列
time = [[] for _ in range(6)]

for i, sig in enumerate(signal):
    time[i] = np.arange(0, len(sig)/fs, 1/fs)
    time[i] = time[i][:len(sig)]
    print(f"PassingTime {i + 1}: {len(sig)/fs} s")

# 結果を表示
for i, t in enumerate(time):
    print(f"time[{i}]: {t[:10]}")  # 最初の10個の値を表示

# グラフのプロット
#fig, ax = plt.subplots(2, 3, figsize=(15, 10))
fig, ax = plt.subplots(2, 3, figsize=(18, 10))

#plt.suptitle(plotTitle, fontsize=16)

# 各信号のプロット
for i in range(6):
    row = i // 3
    col = i % 3
    ax[row, col].plot(time[i], signal[i])
#    ax[row, col].set_title(accTitle[i], fontsize=titleFontSize, loc=titleLoc, x=titlex)
    ax[row, col].set_title(accTitle[i], fontsize=titleFontSize)
    ax[row, col].set_xlabel('Time [s]')
    ax[row, col].set_ylabel('Amplitude')
    ax[row, col].set_ylim(-2048, 2047)
    ax[row, col].grid(True)

# プロットの表示
plt.tight_layout(rect=[0, 0, 1, 0.96])

#plt.tight_layout(rect=[0, 0.03, 1, 0.95])
print("Filename to write: " + writeFile)

plt.savefig(writeFile,format='eps')
plt.savefig(writeFilePrev,format='png')
plt.close()
