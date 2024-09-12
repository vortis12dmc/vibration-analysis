import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

writeFilePass = "/gdsfs/gdsfs/mukai/jr/analyTrainData/output/GCCE2024_Plot/"

# 2行3列の図を作成
fig, axs = plt.subplots(2, 3, figsize=(15, 10))

# 画像ファイルのリスト (2行3列)
image_files = [
    ['image1.eps', 'image2.eps', 'image3.eps'],
    ['image4.eps', 'image5.eps', 'image6.eps']
]

# 画像ファイルを格納
for i in range(2):
    for j in range(3):
        image_files[i][j] = writeFilePass + f"_plot_{i*3 + j}.eps"

# セルに画像をベクター形式で埋め込む
for i in range(2):
    for j in range(3):
        img = mpimg.imread(image_files[i][j])
        imagebox = OffsetImage(img, zoom=0.5)  # 画像のサイズを調整
        ab = AnnotationBbox(imagebox, (0.5, 0.5), frameon=False, box_alignment=(0.5, 0.5))
        axs[i, j].add_artist(ab)
        axs[i, j].axis('off')  # 軸をオフにする

# 表全体の調整
plt.tight_layout()

# 保存
writeFile = writeFilePass + "_repData_v4" + ".eps"
writeFilePrev = writeFilePass + "_repData_v4" + ".png"

plt.savefig(writeFile, format='eps')
plt.savefig(writeFilePrev, format='png')
plt.close()
