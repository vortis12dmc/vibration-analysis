import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import numpy as np
import struct

ylim_range_top = 2057
ylim_range_bottom = -2058

args = sys.argv
arguments_count = len(sys.argv)
if arguments_count < 4:
    print("Usage: "+args[0]+" <信号1の前半> <信号1の後半> <閾値>")
#    print("Usage: "+args[0]+" <信号1の前半> <信号1の後半>")
    sys.exit(1)

readFile1_1 = args[1]
readFile1_2 = args[2]
threshold_val = int(args[3])

# ウィンドウ幅，STFTを施す数の設定 '
t_wndw = 100.0e-3 # 100 milisecond
n_stft = 100 # number of STFT
freq_upper = 3200 # 表示する周波数の上限

extract_t_wndw = 100.0e-3
extract_n_stft = 100

num1 = []
fs = 6400 #サンプリング周波数
axis = readFile1_1[-5].upper()
sprit_readFile = readFile1_1.split('/')

accAxis = "Raw " + axis + "-axis"
fftAxis = "STFT " + axis + "-axis"
thre=int(threshold_val/10)
propaties = axis+"-axis_thre"+str(thre)+"G"
#writeFile = readFile1_1[:-4] + "_STFT_analyPlot.png"
writeFile = readFile1_1[:-4] + "_STFT_analyPlot.svg"

#out_fig_path = "./output/STFT/" + filename1_1[:-4] + "_" + propaties + ".png"
#print(out_fig_path)

"""
accTitle1 = "Raw " +sprit_readFile1[2]+'/'+sprit_readFile1[3]+'/'+ axis1 + "-axis"
accTitle2 = "Raw " +sprit_readFile2[2]+'/'+sprit_readFile2[3]+'/'+ axis2 + "-axis"
powTitle1 = "Pow " +sprit_readFile1[2]+'/'+sprit_readFile1[3]+'/'+ axis1 + "-axis"
powTitle2 = "Pow " +sprit_readFile2[2]+'/'+sprit_readFile2[3]+'/'+ axis2 + "-axis"
plotTitle = sprit_readFile1[2]+'/'+sprit_readFile1[3]+'/'+ axis1 + "-axis" +' & '+sprit_readFile2[2]+'/'+sprit_readFile2[3]+'/'+ axis2 + "-axis_npseg-"+str(npseg)
crosTitle = "Cros " +sprit_readFile1[2]+'/'+sprit_readFile1[3]+'/'+ axis1 + "-axis" +'&'+sprit_readFile2[2]+'/'+sprit_readFile2[3]+'/'+ axis2 + "-axis"
coheTitle = "Coherence " +sprit_readFile1[2]+'/'+sprit_readFile1[3]+'/'+ axis1 + "-axis" +'&'+sprit_readFile2[2]+'/'+sprit_readFile2[3]+'/'+ axis2 + "-axis"
#writeFile = writeFilePass+sprit_readFile1[2]+'_'+sprit_readFile1[3]+'_'+ axis1 + "axis" +'__'+sprit_readFile2[2]+'_'+sprit_readFile2[3]+'_'+ axis2 + "axis" + "_coherence_npseg-"+str(npseg)+".png"
"""
"""
print("Filename1 to read: " + readFile1)
print("Filename2 to read: " + readFile2)
"""

#信号の読み出し
with open(readFile1_1,'rb') as f:
    data1_1 = f.read() #読み出し

for i in range(0, len(data1_1), 2):
    # 2バイト取り出し
    two_bytes = data1_1[i:i+2]
    #print(i)
    (value_1,) = struct.unpack('<h', two_bytes)
    num1.append(value_1)

if readFile1_2 != "none": #信号1の結合作業
    with open(readFile1_2,'rb') as f:
        data1_2 = f.read() #読み出し
    for i in range(0, len(data1_2), 2):
        # 2バイト取り出し
        two_bytes = data1_2[i:i+2]
        #print(i)
        (value_1,) = struct.unpack('<h', two_bytes)
        num1.append(value_1)


data1_d_N = int(len(data1_1)/2) #data1のデータ数
print("The number of top half: " + str(data1_d_N))
#data2_d_N = int(len(data1_2)/2) #data2のデータ数
#print("The number of botom half: " + str(data2_d_N))
data1_d_N = len(num1)  # num1のデータ数
print("The number of data1: " + str(data1_d_N))

signal1=np.array(num1)

#信号の切り出し
print("signal1 切り出し前: "+str(len(num1)))
# 処理：強い振動が起きている範囲の切り出し
# 規定値以上の値が最初に出現するインデックスを検索
start_index = next((i for i, x in enumerate(num1) if x >= threshold_val), None)
# 規定値以上の値が最後に出現するインデックスを検索
end_index = len(num1) - next((i for i, x in enumerate(reversed(num1)) if x >= threshold_val), None)
# 条件に合致する部分リストを抽出
extract_signal1 = np.array(num1[start_index:end_index])
extract_data1_d_N = len(extract_signal1)
print("signal1 切り出し後: "+str(len(extract_signal1)))

print("Sampling frequency: " + str(fs))

#時間軸の計算(生データ)
time1 = np.arange(0, len(signal1)/fs, 1/fs)
time1 = time1[:len(signal1)]
print("PassingTime 1: "+ str(len(signal1)/fs) +" s")

tms=0.0 #サンプリング開始時刻
tme=time1[len(time1)-1]+time1[1] #サンプリング終了時刻

#時間軸の計算(切り出したもの)
extract_time1 = np.arange(0, len(extract_signal1)/fs, 1/fs)
extract_time1 = extract_time1[:len(extract_signal1)]
print("PassingTime(extract) 1: "+ str(len(extract_signal1)/fs) +" s")

extract_tms=0.0 #サンプリング開始時刻
extract_tme=extract_time1[len(extract_time1)-1]+extract_time1[1] #サンプリング終了時刻


"""
短時間フーリエ変換
時間刻み
"""
dt = time1[1] - time1[0]
#入力されたn_wndwをt_wndwで設定した幅より小さい，かつ，2の累乗個に設定する
n_wndw = int(2**(np.floor(np.log2(t_wndw/dt))))
t_wndw = n_wndw*dt # recalculate t_wndw
n_freq = n_wndw

extract_dt = extract_time1[1] - extract_time1[0]
extract_n_wndw = int(2**(np.floor(np.log2(extract_t_wndw/extract_dt))))
extract_t_wndw = extract_n_wndw*extract_dt # recalculate t_wndw\
extract_n_freq = extract_n_wndw

#周波数
freq_sp = np.fft.fftfreq(n_wndw, dt)
extract_freq_sp = np.fft.fftfreq(extract_n_wndw, extract_dt)

#スペクトルを計算する時刻を決める
m = len(time1) - n_wndw
indxs = np.zeros(n_stft, dtype=int)
for i in range(n_stft):
    indxs[i] = int(m/(n_stft+1)*(i+1)) + n_wndw//2

tm_sp = time1[indxs] # DFTをかける時刻の配列

#スペクトルを計算する時刻を決める(切り出し)
m = len(extract_time1) - extract_n_wndw
extract_indxs = np.zeros(extract_n_stft, dtype=int)
for i in range(extract_n_stft):
    extract_indxs[i] = int(m/(extract_n_stft+1)*(i+1)) + extract_n_wndw//2

extract_tm_sp = extract_time1[extract_indxs] # DFTをかける時刻の配列



# スペクトログラムを計算する
# スペクトルは indxs[i] - n_wndw //2 + 1 ~ indxs[i] + n_wndw//2 の n_wndw 幅で行う
sp = np.zeros((n_freq, n_stft), dtype=complex) # スペクトログラムの2次元ndarray  
wndw = np.hamming(n_wndw) # hamming
#wndw = np.hanning(n_wndw) # hanning
#wndw = np.ones(n_wndw)    # 矩形窓
for i in range(n_stft):
    indx = indxs[i] - n_wndw//2 + 1
    sp[:, i] = np.fft.fft(wndw*signal1[indx:indx+n_wndw], n_wndw)/np.sqrt(n_wndw)

# スペクトログラムを計算する(切り出し)
# スペクトルは indxs[i] - n_wndw //2 + 1 ~ indxs[i] + n_wndw//2 の n_wndw 幅で行う
extract_sp = np.zeros((extract_n_freq, extract_n_stft), dtype=complex) # スペクトログラムの2次元ndarray  
wndw = np.hamming(extract_n_wndw) # hamming
#wndw = np.hanning(n_wndw) # hanning
#wndw = np.ones(n_wndw)    # 矩形窓
for i in range(extract_n_stft):
    indx = extract_indxs[i] - extract_n_wndw//2 + 1
    extract_sp[:, i] = np.fft.fft(wndw*extract_signal1[indx:indx+extract_n_wndw], extract_n_wndw)/np.sqrt(extract_n_wndw)





#解析結果の可視化
fig = plt.figure(figsize = (16, 10))

fig.suptitle('[' + sprit_readFile[2] + '] [' + sprit_readFile[3] + '] ' + '[' + axis + '] ' + sprit_readFile[4][:-8])

# サブプロットとカラーバーのための軸を追加
# 各軸の位置は [左, 下, 幅, 高さ] のリストで指定
# 数値はフィギュアサイズに対する比率であることに注意

# 上段のサブプロット
ax_raw = fig.add_axes([0.05, 0.55, 0.25, 0.4])
ax_rawEx = fig.add_axes([0.375, 0.55, 0.25, 0.4])
ax_fftEx = fig.add_axes([0.7, 0.55, 0.25, 0.4])

# 下段のサブプロット
ax_STFT = fig.add_axes([0.05, 0.05, 0.25, 0.4])
ax_STFTEx = fig.add_axes([0.375, 0.05, 0.25, 0.4])
ax_powEx = fig.add_axes([0.7, 0.05, 0.25, 0.4])

# カラーバーのための軸
cb_STFT = fig.add_axes([0.91, 0.55, 0.01, 0.4])
cb_STFTEx = fig.add_axes([0.91, 0.05, 0.01, 0.4])


#元データのプロット
ax_raw.plot(time1, signal1)
ax_raw.grid()
ax_raw.set_title(accAxis, loc='center')
ax_raw.set_ylim(ylim_range_bottom, ylim_range_top)
ax_raw.set_xlabel("Time[s]")
ax_raw.set_ylabel("Acceleration")
ax_raw.set_xlim(tms, tme)

#元データのプロット(切り出し)
ax_rawEx.plot(extract_time1, extract_signal1)
ax_rawEx.grid()
ax_rawEx.set_title(accAxis, loc='center')
ax_rawEx.set_ylim(ylim_range_bottom, ylim_range_top)
ax_rawEx.set_xlabel("Time[s]")
ax_rawEx.set_ylabel("Acceleration")
ax_rawEx.set_xlim(extract_tms, extract_tme)

#スペクトログラムのプロット
ax_STFT.set_xlim(tms, tme)
ax_STFT.set_xlabel('time (s)')
ax_STFT.tick_params(labelbottom=True)
ax_STFT.set_ylim(0, freq_upper)
ax_STFT.set_ylabel('frequency (Hz)')
ax_STFT.set_title(fftAxis, loc='center')

#norm = mpl.colors.Normalize(vmin=np.log10(np.abs(sp[freq_sp < freq_upper, :])**2).min(),
#                            vmax=np.log10(np.abs(sp[freq_sp < freq_upper, :])**2).max())

norm = mpl.colors.Normalize(vmin=-10,
                            vmax=10)


cmap = mpl.cm.jet
ax_STFT.contourf(tm_sp, freq_sp, np.log10(np.abs(sp)**2), 
                    norm=norm,
                    levels=256, 
                    cmap=cmap)
ax_STFT.text(0.99, 0.97, "spectrogram", color='white', ha='right', va='top',
                path_effects=[path_effects.Stroke(linewidth=2, foreground='black'),
                            path_effects.Normal()], 
                transform=ax_STFT.transAxes)
mpl.colorbar.ColorbarBase(cb_STFT, cmap=cmap,
                            norm=norm,

                            orientation="vertical",
                            label='$\log_{10}|X/N|^2$')


cmap = mpl.cm.jet
ax_STFTEx.contourf(extract_tm_sp, extract_freq_sp, np.log10(np.abs(extract_sp)**2), 
                    norm=norm,
                    levels=256, 
                    cmap=cmap)
ax_STFTEx.text(0.99, 0.97, "spectrogram", color='white', ha='right', va='top',
                path_effects=[path_effects.Stroke(linewidth=2, foreground='black'),
                            path_effects.Normal()], 
                transform=ax_STFTEx.transAxes)
mpl.colorbar.ColorbarBase(cb_STFTEx, cmap=cmap,
                            norm=norm,

                            orientation="vertical",
                            label='$\log_{10}|X/N|^2$')
plt.tight_layout()
#plt.show()
#print(a)

print("Filename to write: " + writeFile)
plt.savefig(writeFile)
plt.close()


"""
#-----#
#解析結果の可視化（教科書のフォーマット）
figsize = (210/25.4, 294/25.4)
dpi = 200
fig = plt.figure(figsize=figsize, dpi=dpi)

#図の設定
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['xtick.top'] = True
plt.rcParams['xtick.major.size'] = 6
plt.rcParams['xtick.minor.size'] = 3
plt.rcParams['xtick.minor.visible'] = True
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['ytick.right'] = True
plt.rcParams['ytick.major.size'] = 6
plt.rcParams['ytick.minor.size'] = 3
plt.rcParams['ytick.minor.visible'] = True
plt.rcParams["font.size"] = 14
plt.rcParams['font.family'] = 'Arial'

#窓関数幅をプロット上部に記載
fig.text(0.10, 0.95, f't_wndw = {t_wndw} s, threshold = {thre} G, ')

#プロット枠(axes)の設定 
ax1 = fig.add_axes([0.15, 0.55, 0.70, 0.3])
ax_sp1 = fig.add_axes([0.15, 0.2, 0.70, 0.30])
cb_sp1 = fig.add_axes([0.87, 0.2, 0.02, 0.30])

#元データのプロット
ax1.set_xlim(tms, tme)
ax1.set_xlabel('')
ax1.tick_params(labelbottom=False)
ax1.set_ylabel(str(axis))
ax1.set_ylim(ylim_range_bottom, ylim_range_top)
ax1.plot(time1, signal1, c='black')

#スペクトログラムのプロット
ax_sp1.set_xlim(tms, tme)
ax_sp1.set_xlabel('time (s)')
ax_sp1.tick_params(labelbottom=True)
ax_sp1.set_ylim(0, freq_upper)
ax_sp1.set_ylabel('frequency\n(Hz)')

norm = mpl.colors.Normalize(vmin=np.log10(np.abs(sp[freq_sp < freq_upper, :])**2).min(),
                            vmax=np.log10(np.abs(sp[freq_sp < freq_upper, :])**2).max())
cmap = mpl.cm.jet
ax_sp1.contourf(tm_sp, freq_sp, np.log10(np.abs(sp)**2), 
                    norm=norm,
                    levels=256, 
                    cmap=cmap)
ax_sp1.text(0.99, 0.97, "spectrogram", color='white', ha='right', va='top',
                path_effects=[path_effects.Stroke(linewidth=2, foreground='black'),
                            path_effects.Normal()], 
                transform=ax_sp1.transAxes)
mpl.colorbar.ColorbarBase(cb_sp1, cmap=cmap,
                            norm=norm,
                            orientation="vertical",
                            label='$\log_{10}|X/N|^2$')

#図を保存
plt.savefig(out_fig_path, transparent=False)
#plt.savefig("./output/STFT/20230921.png", transparent=False)
"""
