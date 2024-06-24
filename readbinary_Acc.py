import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import coherence, csd
from scipy import signal
import struct
from matplotlib.ticker import ScalarFormatter


#writeFilePass = "/gdsfs/gdsfs/mukai/jr/analyTrainData/output/coherence/"

ylim_range_top = 2057
ylim_range_bottom = -2058


args = sys.argv
arguments_count = len(sys.argv)
if arguments_count < 3:
#    print("Usage: "+args[0]+" <信号1の前半> <信号1の後半> <閾値>")
    print("Usage: "+args[0]+" <信号1の前半> <信号1の後半>")
    sys.exit(1)

num1 = []

readFile1_1 = args[1]
readFile1_2 = args[2]

fs = 6400 #サンプリング周波数
axis = readFile1_1[-5].upper()
sprit_readFile = readFile1_1.split('/')

accAxis = "Raw " + axis + "-axis"
fftAxis = "FFT " + axis + "-axis"
writeFile = readFile1_1[:-3] + "png"

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

#信号1
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


#data1_d_N = int(len(data1)/2) #data1のデータ数
#data2_d_N = int(len(data2)/2) #data2のデータ数
data1_d_N = len(num1)  # num1のデータ数
#print("The number of data1: " + str(data1_d_N))

signal1=np.array(num1)

print(sprit_readFile[2]+","+sprit_readFile[3]+","+axis+","+str(np.max(signal1))+","+str(np.min(signal1)))

