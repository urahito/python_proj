import os
import csv
import datetime
import tqdm

# MB掛け算
def mul_mega(value):
    return value * pow(1024, 2)

# MB割り算
def div_mega(value):
    return int(value / mul_mega(1))

# MB表示用（引数がB単位）
def str_div_mega(value):
    return str(div_mega(value))

# 操作できないフォルダを指定
def is_exclude_path(path):
    # 'Program Files'は空白を認識してくれないらしく、これで妥協
    exclude_list = ['C:\\Program', 'C:\\Windows', 'AppData']
    for target_path in exclude_list:
        if target_path in path:
            return True
    return False

# ユーザーフォルダ以下のpathにタグを付ける（pathに含まれればそのまま）
def get_special_path(path):
    # iTunesは必ずMusicの前に置かないと分類できない
    special_path_list = ['iTunes', 'Music', 'Videos', 'Pictures', 'Documents', 'Downloads']
    for spectial_tag in special_path_list:
        if spectial_tag in path:
            return spectial_tag
    return 'Other'

# mainメソッド
def main():
    # 100MB以上の定数値代わり
    big_size = mul_mega(100)

    # 現在時刻の取得（結果出力ファイル名に利用）
    now_time = datetime.datetime.now()
    now_str = now_time.strftime('%Y%m%d%H%M%S')

    # 結果出力ファイルの設定(csv)
    output_file = open('result' + now_str + '.csv', 'w', newline='', encoding='utf-8')
    output_writer = csv.writer(output_file)

    # ヘッダの設定
    output_writer.writerow(['filename', 'extention', 'Media', 'size(MB)', 'dirpath', 'fullpath'])

    # フォルダの走査
    for foldername, subfolders, filenames in tqdm.tqdm(os.walk('C:\\')):
        sum_size = 0

        if is_exclude_path(foldername):
            continue

        # ファイル単位のリストアップ
        for filename in filenames:
            try:
                # フルパスを取得
                full_path = os.path.join(foldername, filename)

                # 存在するファイルの場合
                if os.path.exists(full_path) and os.path.isfile(full_path):
                    # ファイルサイズを取得
                    file_size = os.path.getsize(full_path)
                    sum_size += file_size

                    # 拡張子を取得する(ext)
                    root, ext = os.path.splitext(full_path)

                    # ファイルサイズが100MB以上の場合、かつ拡張子がある場合
                    if file_size >= big_size and len(ext) > 0:
                        # csvファイルに書き出す
                        output_writer.writerow([filename, ext, get_special_path(full_path), 
                                                str_div_mega(file_size), foldername, full_path])
            except FileNotFoundError:
                print('FILE ERROR: ' + filename)
            except EnvironmentError:
                print('ENCODE ERROR: ' + filename)

        # フォルダサイズの出力
        if sum_size >= big_size:
            output_writer.writerow([foldername, 'dir', get_special_path(full_path), 
                                    str_div_mega(sum_size), foldername, foldername])
    # 結果ファイルを閉じて保存する
    output_file.close()

main()