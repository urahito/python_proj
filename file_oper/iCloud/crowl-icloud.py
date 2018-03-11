# -- coding: utf-8 --
import configparser
from operator import attrgetter
import sys, os
import time
from pathlib import Path
sys.path.append(os.getcwd())
from file_attr import file_attr

# iniファイルから色々読み込む
def get_ini_data(path_obj):
    ini_file = configparser.SafeConfigParser()

    with path_obj.open('r', encoding='utf-8') as ini_file_obj:        
        ini_file.read_file(ini_file_obj)

    return ini_file

def append_to_list(flist, input_dir, pattern_list):
    for pattern in pattern_list:
        for path in list(input_dir.glob(pattern)):
            flist.append(path)
    return flist

def get_files(input_dir, output_dir):
    files = []
    file_list = []
    file_list = append_to_list(file_list, input_dir, ['*.gif', '*.PNG'])

    for file_path in file_list:
        files.append(file_attr(file_path, output_dir))

    return sorted(files, key=attrgetter("create_time"))

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
    output_dir = Path(ini_data['settings']['output'])
    print(input_dir)
    files = get_files(input_dir, output_dir)

    for fi in files:
        print(fi)
    
    # 特定したファイルを一時フォルダへ

    # 一時フォルダをzip化する

    # zipファイルをDドライブの専用フォルダへ移動する

if __name__ == '__main__':
    main()