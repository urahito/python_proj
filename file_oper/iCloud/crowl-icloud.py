import configparser
import sys, os
from pathlib import Path

# iniファイルから色々読み込む
def get_ini_data(path_obj):
    ini_file = configparser.SafeConfigParser()

    with path_obj.open('r', encoding='utf-8') as ini_file_obj:        
        ini_file.read_file(ini_file_obj)

    return ini_file

def get_files(input_dir):
    files = {}
    for gif_file in list(input_dir.glob('*.gif')):
        files[gif_file] = os.path.getsize(gif_file)

    for png_file in list(input_dir.glob('*.PNG')):
        files[png_file] = os.path.getsize(png_file)
    
    print(str(len(files)) + '(flies)')
    print(str(sum(files.values()) / (1024 ** 2)) + '(MB)')

    return files

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