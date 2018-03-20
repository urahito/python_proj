# -- coding: utf-8 --
# 操作系
import configparser
from operator import attrgetter
from pathlib import Path
import tqdm
from tempfile import TemporaryDirectory as Tempdir
from Pillow import Image
from zipfile import Zipfile
# 基本ライブラリ
import sys, os
from datetime import datetime as ddt
from datetime import timedelta as dlt
import csv
# 外部クラス
sys.path.append(os.getcwd())
from file_attr import file_attr
from logger_setting import logger_setting as logger_s

# ログ代わりの出力結果csvの出力
def output_csv_log(files, input_dir, output_dir, csv_sub):
    # ログファイル名
    now_str = file_attr.get_datetime_str(ddt.now(), '%Y%m%d-%H%M%S')
    csv_name = 'result-{}.csv'.format(now_str)
    # ログフォルダ
    log_dir = file_attr.make_parent_dir(output_dir, csv_sub)

    out_csv = log_dir / csv_name
    print('log file: ' + str(out_csv))

    with out_csv.open('w', encoding=file_attr.get_enc('w'), newline='') as out_file_obj:
        csv_obj = csv.writer(out_file_obj, dialect='excel')

        csv_obj.writerow(['対象フォルダ', input_dir])
        csv_obj.writerow(['転送先フォルダ', output_dir])
        csv_obj.writerow([''])
        csv_obj.writerow(['ファイル名', '作成日時', '(KB)', '転送先フォルダ', '転送対象'])

        for fi in tqdm.tqdm(files):
            csv_obj.writerow(fi.output_line())

# zipファイルをDドライブの専用フォルダへ移動する
def move_zip(zip_path, dest_dir):
    print('')

# 一時フォルダをzip化する
def comp_to_zip(target_dir, dest_path):
    print('')

# GIFアニメーションを作成する
def make_gif_animation(target_dir, dest_path):
    print('')

# GIFのコピーを作る（GIFアニメーション用）
def get_gif_copy(files):
    # GIF用の一時フォルダも必要
    print('')

# 特定したファイルを一時フォルダへ
def move_to_temp_dir(files, target_dir):
    print('')

# 古いファイルを特定する(1年以上前なら500MBまで)
def get_old_pictures(files):
    size_sum = 0
    past_ng = False

    for fi in tqdm.tqdm(files):
        size_sum, past_ng = fi.allow_file_copy(size_sum, 90, past_ng)

# ファイルパターンを指定して、入力フォルダからのファイルを絞り込む
def append_to_list(flist, input_dir, pattern_list):
    for pattern in pattern_list:
        for path in list(input_dir.glob(pattern)):
            flist.append(path)
    return flist

# ファイル情報の取得
def get_files(input_dir, output_dir):
    files = []
    file_list = []
    file_list = append_to_list(file_list, input_dir, ['*.gif', '*.PNG'])
    size_max = file_attr.get_big_size(500, 'MB')

    for file_path in tqdm.tqdm(file_list):
        files.append(file_attr(file_path, output_dir, size_max))

    return sorted(files, key=attrgetter("create_time"))

# iniファイルから色々読み込む
def get_ini_data(path_obj, ini_name):
    ini_file = configparser.SafeConfigParser()

    if not path_obj.exists():
        print('ファイル名を{}にしてください', ini_name)
        return None

    with path_obj.open('r', encoding='utf-8') as ini_file_obj:        
        ini_file.read_file(ini_file_obj)

    return ini_file

def main():
    # iniファイルの準備
    ini_name = 'for-iCloud.ini'
    ini_path = Path(__file__).parent / ini_name
    ini_data = get_ini_data(ini_path, ini_name)

    if ini_data == None:
        return

    # 古いファイルを特定する(1年以上前なら1GBまで)
    input_dir = Path(ini_data['settings']['input'])
    output_dir = Path(ini_data['settings']['output'])
    print(input_dir)

    # loggerの取得
    logger = logger_s(ini_data)

    # ファイルリストの取得
    files = get_files(input_dir, output_dir)
    
    # ファイルの仕分け
    get_old_pictures(files)
    
    # ファイル移動関係は、エラー時もログファイルを出力する
    try:
        now_str = file_attr.get_datetime_str(ddt.now(), '%Y%m%d-%H%M%S')

        # 特定したファイルを一時フォルダへ

        # GIFのコピーを作る（GIFアニメーション用）

        # GIFアニメーションを作成する

        # 一時フォルダをzip化する

        # zipファイルをDドライブの専用フォルダへ移動する
    finally:
        # ログファイルの出力
        csv_sub = ini_data['log']['csv']
        output_csv_log(files, input_dir, output_dir, csv_sub)
    print('finished')

if __name__ == '__main__':
    main()