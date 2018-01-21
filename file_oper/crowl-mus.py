import os
import csv
import datetime
import tqdm

# MB掛け算
def mul_mega(value):
    return value * (1024 ** 2)

# MB割り算
def div_mega(value):
    return int(value / mul_mega(1))

# MB表示用（引数がB単位）
def str_div_mega(value):
    return replace_str(str(div_mega(value)))

#replaceメソッド
def replace_str(target_str):
    # 出力時にエンコードエラーとなる文字列を随時追記
    replace_list = ['\xe9']
    for rep_str in replace_list:
        target_str = target_str.replace(rep_str, '')
    return target_str

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
    # 現在時刻の取得（結果出力ファイル名に利用）
    now_time = datetime.datetime.now()
    now_str = now_time.strftime('%Y%m%d%H%M%S')

    # 結果出力ファイルの設定(csv)
    output_file = open('result' + now_str + '.csv', 'w', newline='')
    output_writer = csv.writer(output_file)

    # ヘッダの設定
    output_writer.writerow(['filename', 'extention', 'Media', 'dirpath', 'fullpath'])

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
                    # 拡張子を取得する(ext)
                    root, ext = os.path.splitext(full_path)

                    # ファイルサイズが100MB以上の場合、かつ拡張子がある場合
                    if ext == '.mus':
                        # csvファイルに書き出す
                        output_writer.writerow([replace_str(filename), replace_str(ext), \
                                                get_special_path(full_path),  \
                                                replace_str(foldername), replace_str(full_path)])
            except FileNotFoundError:
                print('FILE ERROR: ' + filename)
            except EnvironmentError:
                print('ENCODE ERROR: ' + filename)
    
    # フォルダの走査
    for foldername, subfolders, filenames in tqdm.tqdm(os.walk('D:\\')):
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
                    # 拡張子を取得する(ext)
                    root, ext = os.path.splitext(full_path)

                    # ファイルサイズが100MB以上の場合、かつ拡張子がある場合
                    if ext == '.mus':
                        # csvファイルに書き出す
                        output_writer.writerow([replace_str(filename), replace_str(ext), \
                                                get_special_path(full_path),  \
                                                replace_str(foldername), replace_str(full_path)])
            except FileNotFoundError:
                print('FILE ERROR: ' + filename)
            except EnvironmentError:
                print('ENCODE ERROR: ' + filename)

    # 結果ファイルを閉じて保存する
    output_file.close()

main()