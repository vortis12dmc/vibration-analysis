import numpy as np
import matplotlib.pyplot as plt
import struct
import sys

from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

writeFilePass = "/gdsfs/gdsfs/mukai/jr/analyTrainData/output/GCCE2024_Plot/rep/rainy/"

titleFontSize = 16
args = sys.argv
arguments_count = len(sys.argv)
if arguments_count < 13:
    print("Usage: "+args[0]+" <信号1の前半> <信号1の後半> <信号2の前半> <信号2の後半> <信号3の前半> <信号3の後半> <信号4の前半> <信号4の後半> ・・・ <信号6の後半>")
    sys.exit(1)

num = [[] for _ in range(6)]

readFile = [
    [args[1], args[2]],
    [args[3], args[4]],
    [args[5], args[6]],
    [args[7], args[8]],
    [args[9], args[10]],
    [args[11], args[12]]
]

fs = 6400 #サンプリング周波数

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

writeFile = writeFilePass + "_repData_v3" + split_readFile[0][2] + ".eps"
writeFilePrev = writeFilePass + "_repData_v3" + split_readFile[0][2] + ".png"

def replace_strings(s):
    s = s.replace("A_", "N_")
    s = s.replace("B_", "F_")
    s = s.replace("In", "Left")
    s = s.replace("Out", "Right")
    return s

sensorNameGCCE = [replace_strings(entry[3]) for entry in split_readFile]

accTitle = [
    "Raw " + split_readFile[0][2] + '/' + sensorNameGCCE[0] + '/' + axis[0] + "-axis",
    "Raw " + split_readFile[1][2] + '/' + sensorNameGCCE[1] + '/' + axis[1] + "-axis",
    "Raw " + split_readFile[2][2] + '/' + sensorNameGCCE[2] + '/' + axis[2] + "-axis",
    "Raw " + split_readFile[3][2] + '/' + sensorNameGCCE[3] + '/' + axis[3] + "-axis",
    "Raw " + split_readFile[4][2] + '/' + sensorNameGCCE[4] + '/' + axis[4] + "-axis",
    "Raw " + split_readFile[5][2] + '/' + sensorNameGCCE[5] + '/' + axis[5] + "-axis"
]

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

for idx, file_pair in enumerate(readFile):
    process_files(file_pair, num[idx])

threshold_val=50

signal = [[] for _ in range(6)]

for i, num_list in enumerate(num):
    print(f"signal{i + 1} 処理前: {len(num_list)}")
    start_index = next((i for i, x in enumerate(num_list) if x >= threshold_val), None)
    end_index = len(num_list) - next((i for i, x in enumerate(reversed(num_list)) if x >= threshold_val), None)
    if start_index is not None and end_index is not None:
        signal[i] = np.array(num_list[start_index:end_index])
    print(f"signal{i + 1} 処理後: {len(signal[i])}")

print("Sampling frequency: " + str(fs))

time = [[] for _ in range(6)]

for i, sig in enumerate(signal):
    time[i] = np.arange(0, len(sig)/fs, 1/fs)
    time[i] = time[i][:len(sig)]
    print(f"PassingTime {i + 1}: {len(sig)/fs} s")

for i, t in enumerate(time):
    print(f"time[{i}]: {t[:10]}")

# 各プロットを個別の画像ファイルとして保存
for i in range(6):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(time[i], signal[i])
    ax.set_title(accTitle[i], fontsize=titleFontSize)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Amplitude')
    ax.set_ylim(-2048, 2047)
    ax.grid(True)
    plot_filename = writeFilePass + f"_plot_{i}.eps"
    plt.savefig(plot_filename, format='eps')
    plt.close()


"""
# 表の作成
fig, axarr = plt.subplots(2, 3, figsize=(18, 8))
plt.subplots_adjust(wspace=0.1, hspace=0.2)

# 各セルに画像を配置
for i in range(2):
    for j in range(3):
        img = mpimg.imread(writeFilePass + f"_plot_{i*3 + j}.eps")
        axarr[i, j].imshow(img)
        axarr[i, j].axis('off')

# 行と列のラベルを追加
col_labels = ['Left rail', 'Right rail', 'Signal bond']
row_labels = ['Point N', 'Point F']

for ax, col in zip(axarr[0], col_labels):
    ax.set_title(col, fontsize=titleFontSize)

for ax, row in zip(axarr[:, 0], row_labels):
    ax.set_ylabel(row, fontsize=titleFontSize, rotation=0, labelpad=60, va='center')

# PDFとして保存
pdf_filename = writeFilePass + "_table_with_plots.pdf"
with PdfPages(pdf_filename) as pdf:
    pdf.savefig(fig)

plt.close()
"""

# 表の作成
fig, axarr = plt.subplots(2, 3, figsize=(18, 8))
plt.subplots_adjust(wspace=0.1, hspace=0.1)

# 各セルに画像を配置
for i in range(2):
    for j in range(3):
        plot_filename = writeFilePass + f"_plot_{i*3 + j}.eps"
        img = plt.imread(plot_filename)
        imagebox = OffsetImage(img, zoom=0.8)
        ab = AnnotationBbox(imagebox, (0.5, 0.5), frameon=False, box_alignment=(0.5, 0.5))
        axarr[i, j].add_artist(ab)
        axarr[i, j].axis('off')

# 行と列のラベルを追加
col_labels = ['Left rail', 'Right rail', 'Signal bond']
row_labels = ['Point N', 'Point F']

for ax, col in zip(axarr[0], col_labels):
    ax.set_title(col, fontsize=titleFontSize)

for ax, row in zip(axarr[:, 0], row_labels):
    ax.set_ylabel(row, fontsize=titleFontSize, rotation=0, labelpad=10, va='center')

# PDFとして保存
pdf_filename = writeFilePass + "_table_with_plots.pdf"
with PdfPages(pdf_filename) as pdf:
    pdf.savefig(fig)

plt.close()
