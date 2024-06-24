import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft
import struct

args = sys.argv
arguments_count = len(sys.argv)
if arguments_count < 3:
    print("Usage: "+args[0]+" <信号1の前半>")
#    print("Usage: "+args[0]+" <信号1の前半> <信号1の後半>")
    sys.exit(1)

readFile1_1 = args[1]
threshold_val = int(args[2])

writeFile = readFile1_1[:-4] + "_STFT_chatGPTSample.png"

# パラメータ設定
fs = 6400  # サンプリング周波数
t_wndw = 0.1  # 窓の時間幅を秒で指定
n_wndw = int(fs * t_wndw)  # 窓のサンプル数を計算

# データの読み込み
with open(readFile1_1, 'rb') as f:
    data = f.read()

# 2バイトごとに整数に変換
num = [struct.unpack('<h', data[i:i+2])[0] for i in range(0, len(data), 2)]

# データの配列化
signal = np.array(num)

# STFTの計算
f, t, Zxx = stft(signal, fs, window='hamming', nperseg=n_wndw)

# STFTのプロット
plt.figure(figsize=(10, 6))
plt.pcolormesh(t, f, np.abs(Zxx), shading='gouraud')
plt.title('STFT Magnitude')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.colorbar(label='Magnitude')

plt.savefig(writeFile)
print("Filename to write: " + writeFile)
plt.close()
