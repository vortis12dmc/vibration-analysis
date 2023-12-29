import os
from PIL import Image, ImageDraw, ImageFont

sub_folders_list = [
    'A_In_Rail',
    'A_Out_Rail',
    'A_Out_Bond',
    'B_In_Rail',
    'B_Out_Rail',
    'B_Out_Bond'
]

output_pdf = './20230921_all_trains_w_name_concat_db_v3.pdf'  # 出力するPDFファイルのパスを指定
#output_pdf = './20230921_All_A_Out_Bond-Rail.pdf'  # 出力するPDFファイルのパスを指定

def get_folders_in_directory(directory_path):
    """指定したディレクトリ内のフォルダのリストを返す関数"""
    try:
        items = os.listdir(directory_path)
        folders = [item for item in items if os.path.isdir(os.path.join(directory_path, item))]
        return folders
    except FileNotFoundError:
        print(f"Error: '{directory_path}' not found.")
        return []

def add_text_to_image(image, text):
    """画像にテキストを追加する関数"""
    draw = ImageDraw.Draw(image)


    # フォントの設定
    # システムのデフォルトのTTFフォントを指定し、サイズを40に設定
    # フォントの設定 (デフォルトフォントを使用)
    #font = ImageFont.load_default()
    #font_path = "/usr/share/fonts/dejavu/DejaVuSansMono-Bold.ttf"
    #font_path = "/usr/share/fonts/dejavu/DejaVuSansMono.ttf"
    font_path = "/usr/share/fonts/google-droid/DroidSans.ttf"
    font = ImageFont.truetype(font_path, 20)  # こちらは一例としてのフォントパスとサイズです
    
    # テキストの位置と色の設定
    text_position = (20, 8)  # 例: 左上の10, 10の位置
    #text_color = (255, 255, 255)  # 白色
    text_color = (0, 0, 0)

    draw.text(text_position, text, font=font, fill=text_color)

    return image

    
top_folder = "../concatTrains"  # ここに目的のフォルダ名を指定
folders_list = get_folders_in_directory(top_folder)
#print(folders_list)

png_files = []
for folder in folders_list:
    print(folder)
    for sub_folder in sub_folders_list:
        folder_path = top_folder + "/" + folder + "/" + sub_folder + "/"
        # フォルダ内のpngファイルのリストを取得
        png_files.extend([folder_path + f for f in os.listdir(folder_path) if f.endswith('_db.png')])
png_files.sort()  # 必要に応じてファイルの順番をソート
print(png_files)


merged_images = []

# 3つずつのグループに分けて画像を結合
for i in range(0, len(png_files), 3):
    group = png_files[i:i+3]
    images = [Image.open(file) for file in group]
    
    # 3つのPNGを垂直に結合
    total_height = sum(img.height for img in images)
    max_width = max(img.width for img in images)
    
    combined_image = Image.new('RGB', (max_width, total_height))
    y_offset = 0
    for img in images:
        combined_image.paste(img, (0, y_offset))
        y_offset += img.height

    text_to_add = png_files[i].split('/')[2] + "  " + png_files[i].split('/')[3]
    merged_images.append(add_text_to_image(combined_image, text_to_add))
        
# 結合した画像をPDFに変換
if merged_images:
    merged_images[0].save(output_pdf, save_all=True, append_images=merged_images[1:])
    print(f"Saved to {output_pdf}")
            
