from PIL import Image
import os

def pngs_to_pdf_sorted(directory, output_pdf):
    # ディレクトリ内のPNGファイルを取得し、ファイル名の最初の4桁に基づいてソート
    png_files = [file for file in os.listdir(directory) if file.endswith('.png')]
    sorted_png_files = sorted(png_files, key=lambda x: x.split('_')[0])

    # ソートされた画像を開く
    images = [Image.open(os.path.join(directory, file)).convert('RGB') for file in sorted_png_files]

    if not images:
        print("指定されたフォルダにPNG画像がありません。")
        return

    # 最初の画像をPDFの最初のページとして保存し、残りの画像を追加
    images[0].save(output_pdf, save_all=True, append_images=images[1:])

directory = './'  # PNG画像が保存されているディレクトリのパス
output_pdf = 'output.pdf'  # 出力PDFの名前

pngs_to_pdf_sorted(directory, output_pdf)

