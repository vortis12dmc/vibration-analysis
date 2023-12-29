import os

# 列車名のリスト
train_names=(
    "0418_K000",
    "1004_S548_R06",
    "1504_S560_R02",
    "1920_T332_U01",
    "0608_S540_S19",
    "1020_T312_U01",
    "1520_T322_U03",
    "1938_S572_R05",
    "0630_T300_U06",
    "1039_S550_R05",
    "1542_S562_R08",
    "1956_T334_U03",
    "0701_S400_U01",
    "1116_M606_R03",
    "1550_T324_U07",
    "2035_M614_S08",
    "0707_T302_R08",
    "1120_T314_U08",
    "1604_S564_S18",
    "2038_T336_U06",
    "0719_M600_R10",
    "1142_S552_S08",
    "1620_T326_U06",
    "2111_S406_S02",
    "0727_T304_U09",
    "1150_U5960A_S13",
    "1642_S566_S11",
    "2156_T338_S03",
    "0742_S542_S15",
    "1211_U3960A_R07",
    "1704_S568_S19",
    "2234_T340_R03",
    "0745_T306_U03",
    "1220_T316_U09",
    "1720_T328_U09",
    "2317_S408_S16",
    "0806_T308_U08",
    "1242_S554_S03",
    "1747_M608_S15",
    "0819_M602_S17",
    "1317_S402_S07",
    "1804_S570_S01",
    "0839_S544_S01",
    "1320_T318_U06",
    "1820_T330_U07",
    "0916_M604_S02",
    "1342_S556_S16",
    "1840_M610_R01",
    "0920_T310_U07",
    "1420_T320_U08",
    "1902_S404_U08",
    "0939_S546_S05",
    "1442_S558_R04",
    "1913_M612_S05"
)


# センサ名のリスト
sensor_names=(
    "A_In_Rail",
    "A_Out_Bond",
    "A_Out_Rail",
    "B_In_Rail",
    "B_Out_Bond",
    "B_Out_Rail"
)

# 基本ディレクトリ（列車名のディレクトリが含まれているディレクトリ）
base_dir = "./"  # このパスは実際の環境に合わせて調整してください

for train in train_names:
    for sensor in sensor_names:
        sensor_dir = os.path.join(base_dir, train, sensor)
        if os.path.exists(sensor_dir):
            print(f"Processing directory: {sensor_dir}")
            for filename in os.listdir(sensor_dir):
                old_file = os.path.join(sensor_dir, filename)
                new_file = os.path.join(sensor_dir, f"{train}_{sensor}_{filename}")
                print(f"Renaming {old_file} to {new_file}")
                os.rename(old_file, new_file)
        else:
            print(f"Directory does not exist: {sensor_dir}")
