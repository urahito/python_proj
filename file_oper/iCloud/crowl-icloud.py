import configparser
import sys, os
import time
from pathlib import Path
import file_attr

# iniファイルから色々読み込む
def get_ini_data(path_obj):
    ini_file = configparser.SafeConfigParser()

    with path_obj.open('r', encoding='utf-8') as ini_file_obj:        
        ini_file.read_file(ini_file_obj)

    return ini_file

def get_files(input_dir):
    files = {}
    for gif_file in list(input_dir.glob('*.gif')):
        files[gif_file] = time.localtime(os.path.getmtime(gif_file))

    for png_file in list(input_dir.glob('*.PNG')):
        files[png_file] = time.localtime(os.path.getmtime(png_file))
    
    print(str(len(files)) + '(flies)')
    print(min(files.values()))

    return sorted(files, key=lambda time: files.values())

# zipファイルをDドライブの専用フォルダへ移動する
def move_zip(zip_file, dest_dir):
    print('')

# 一時フォルダをzip化する
def comp_to_zip(target_dir):
    print('')

# 特定したファイルを一時フォルダへ
def move_to_temp_dir(files, target_dir):
    print('')

# 古いファイルを特定する(1年以上前なら1GBまで)
def get_old_pictures(target_dir):
    print('')

def main():
    # iniファイルの準備
    ini_path = Path(__file__).parent / 'for-iCloud.ini'
    ini_data = get_ini_data(ini_path)

    # 古いファイルを特定する(1年以上前なら1GBまで)
    input_dir = Path(ini_data['settings']['input'])
    print(input_dir)
    files = get_files(input_dir)
    
    # 特定したファイルを一時フォルダへ

    # 一時フォルダをzip化する

    # zipファイルをDドライブの専用フォルダへ移動する

if __name__ == '__main__':
    main()