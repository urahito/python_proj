# -- coding: utf-8 --
# 操作系
import configparser
from operator import attrgetter
from pathlib import Path
import tqdm
# 基本ライブラリ
import sys, os
import datetime
import csv
# 外部クラス
sys.path.append(os.getcwd())
from file_attr import file_attr

# ログ代わりの出力結果csvの出力
def output_csv_log(files, input_dir, output_dir):
    csv_name = 'result-{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
    log_dir = output_dir / 'log'
    log_dir.mkdir(exist_ok=True)

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
def move_zip(zip_file, dest_dir):
    print('')

# 一時フォルダをzip化する
def comp_to_zip(target_dir):
    print('')

# 特定したファイルを一時フォルダへ
def move_to_temp_dir(files, target_dir):
    print('')

# 古いファイルを特定する(1年以上前なら500MBまで)
def get_old_pictures(files):
    size_sum = 0
    size_max = file_attr.get_big_size(500, 'MB')
    found_ng = False

    for fi in files:
        size_sum, found_ng = fi.allow_file_copy(size_sum, size_max, found_ng)

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

    for file_path in tqdm.tqdm(file_list):
        files.append(file_attr(file_path, output_dir))

    return sorted(files, key=attrgetter("create_time"))

# iniファイルから色々読み込む
def get_ini_data(path_obj):
    ini_file = configparser.SafeConfigParser()

    with path_obj.open('r', encoding='utf-8') as ini_file_obj:        
        ini_file.read_file(ini_file_obj)

    return ini_file

def main():
    # iniファイルの準備
    ini_path = Path(__file__).parent / 'for-iCloud.ini'
    ini_data = get_ini_data(ini_path)

    # 古いファイルを特定する(1年以上前なら1GBまで)
    input_dir = Path(ini_data['settings']['input'])
    output_dir = Path(ini_data['settings']['output'])
    print(input_dir)

    # ファイルリストの取得
    files = get_files(input_dir, output_dir)
    
    # ファイルの仕分け
    get_old_pictures(files)
    
    # ファイル移動関係は、エラー時もログファイルを出力する
    try:
        print('')
        # 特定したファイルを一時フォルダへ

        # 一時フォルダをzip化する

        # zipファイルをDドライブの専用フォルダへ移動する
    finally:
        # ログファイルの出力
        output_csv_log(files, input_dir, output_dir)
    print('finished')

if __name__ == '__main__':
    main()