# -- coding: utf-8 --
# 操作系
import configparser
import tqdm
import shutil
from operator import attrgetter
from pathlib import Path
from PIL import Image
from zipfile import ZipFile
# ログ系
import logging
logger = None
# 基本ライブラリ
import sys, os, csv, time
from datetime import datetime as ddt
from datetime import timedelta as dlt
# 外部クラス
sys.path.append(os.getcwd())
from file_attr import file_attr
from logger_setting import logger_setting as logger_s

# info_dicに貯めた情報を出力する
def output_logger(logger, info_dic, time_dic):
    for key in info_dic.keys():
        logger.info('{}: {}'.format(key, info_dic[key]))
    prev_time = 0
    for key in time_dic.keys():
        time_dlt = dlt(seconds=time_dic[key] - prev_time)
        logger.info('{}: {:.1f}(s)'.format(key, time_dlt.total_seconds()))
        prev_time = time_dic[key]

# ログ代わりの出力結果csvの出力
def output_csv_log(files, output_dir, csv_sub):
    # ログファイル名
    now_str = file_attr.get_datetime_str(ddt.now(), '%Y%m%d-%H%M%S')
    csv_name = 'result-{}.csv'.format(now_str)
    # ログフォルダ
    log_dir = file_attr.make_parent_dir(output_dir, csv_sub)

    out_csv = log_dir / csv_name
    print('log file: ' + str(out_csv))

    with out_csv.open('w', encoding=file_attr.get_enc('w'), newline='') as out_file_obj:
        csv_obj = csv.writer(out_file_obj, dialect='excel')
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
def make_gif_animation(out_gifs, dest_dir, now_str, thumb_max, dul_ms=100):
    out_path = Path(dest_dir) / 'thumb-{}.gif'.format(now_str)
    i = 0

    print('サムネイルGIFアニメの保存')
    try:
        out = Image.new('RGB', (thumb_max, thumb_max), (255, 255, 255))

        img_flms = []
        for fi in tqdm.tqdm(out_gifs):
            try:    
                im = Image.open(fi)
                while True:                                        
                    new_frame = Image.new('RGBA', im.size)
                    new_frame.paste(im, (0, 0), im.convert('RGBA'))
                    img_flms.append(new_frame)
                    im.seek(im.tell() + 1)
            except EOFError:
                pass
            try:
                os.remove(fi)
            except Exception:
                pass
        
        print('サムネイルGIFアニメの保存-saving...')
        out.save(out_path, save_all=True, append_images=img_flms[1:], optimize=False, duration=dul_ms, loop=0)
    except:
        raise

# GIFのコピーを作る（GIFアニメーション用） 
def save_to_gif(backup_dir, gif_dir, thumb_max): 
    png_files = list(Path(backup_dir).glob('*.PNG'))
    org_gifs = list(Path(backup_dir).glob('*.gif'))
    out_gifs = []
    wide_size = 0
    
    print('既にあったgifファイルは先に専用フォルダへ')
    for fi in tqdm.tqdm(org_gifs):
        try:
            shutil.move(fi, str(gif_dir / Path(fi).name))
        except:
            raise

    print('PNGファイルをリサイズしてgifファイルへ保存') 
    for fi in tqdm.tqdm(png_files):        
        gif_path = fi.with_suffix('.gif')

        try:
            img = Image.open(fi)
            # ファイルのリサイズ
            wide_size = max([img.width, img.height])
            wide_rate = max([wide_size / thumb_max, 1])
            img_resize = img.resize((int(img.width / wide_rate), int(img.height/wide_rate)))
            # 保存
            img_resize.save(gif_path, 'gif')
        except:
            raise
        # GIFアニメーション用にリスト化
        out_gifs.append(gif_path)

    return out_gifs, png_files

# 特定したファイルを一時フォルダへ
def move_files(files, dest_dir, logger): 
    print('一時ファイルへの移動...')

    for fi in tqdm.tqdm(files):
        # 存在しないファイルは警告して飛ばす
        if not Path(fi.org_path).exists():
            logger.warn("not exist file! {}".format(fi))
            continue
        # 送信先を指定してコピー
        dest_path = Path(dest_dir) / fi.org_path.name
        try:
            shutil.copy2(fi.org_path, dest_path)
        except:
            raise

# 古いファイルを特定する(1年以上前なら500MBまで)
def get_old_pictures(files, size_max):
    print('ファイルの特定の開始...')
    size_sum = 0
    past_ng = False

    for fi in tqdm.tqdm(files):
        file_size = fi.allow_file_copy(90, past_ng)
        if size_max < size_sum:
            past_ng = True
        else:
            size_sum = size_sum + file_size

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

    print('ファイル情報の取得')
    for file_path in tqdm.tqdm(file_list):
        files.append(file_attr(file_path, output_dir))

    return sorted(files, key=attrgetter("create_time"))

# ディレクトリ取得
def get_dirs(ini_data):
    input_dir = Path(ini_data['settings']['input'])
    output_dir = Path(ini_data['settings']['output'])
    backup_dir = file_attr.make_parent_dir(output_dir / ini_data['picture']['backup'])
    gif_dir = file_attr.make_parent_dir(output_dir / ini_data['picture']['gif']) 
    return input_dir, output_dir, backup_dir, gif_dir

# 記録を取る
def rec_time(dic, key, start, logger):
    dic[key] = time.time() - start
    logger.info('{} 完了'.format(key))

# iniファイルから色々読み込む
def get_ini_data(path_obj, ini_name):
    ini_data = configparser.SafeConfigParser()

    if not path_obj.exists():
        print('ファイル名を{}にしてください', ini_name)
        return None

    with path_obj.open('r', encoding='utf-8') as ini_file_obj:        
        ini_data.read_file(ini_file_obj)

    return ini_data

def main():
    # csvへの情報用dict
    info_dic = {}
    time_dic = {}
    time_dic['処理開始'] = time.time()
    time_start = time_dic['処理開始']
    now_str = file_attr.get_datetime_str(ddt.now(), '%Y%m%d-%H%M%S')

    # iniファイルの準備
    ini_name = 'for-iCloud.ini'
    ini_path = Path(__file__).parent / ini_name
    ini_data = get_ini_data(ini_path, ini_name)

    if ini_data == None:
        return

    # loggerの取得
    logger = logger_s(ini_data, __name__, now_str)
    logger.info('初期設定 開始')

    # ディレクトリの取得
    input_dir, output_dir, backup_dir, gif_dir = get_dirs(ini_data)
    info_dic['対象フォルダ'] =  input_dir
    info_dic['転送先フォルダ'] =  output_dir

    # 取り込みファイルの最大値を決める
    size_mb = int(ini_data['settings']['size_mb'])
    size_max = file_attr.get_big_size(size_mb, 'MB')
    info_dic['取り込み最大値'] = '{}(MB)'.format(size_mb)

    # サムネイルの幅を決める
    thumb_max = int(ini_data['picture']['thumb_px'])
    rec_time(time_dic, '初期設定', time_start, logger)

    # ファイルリストの取得
    files = get_files(input_dir, output_dir)
    rec_time(time_dic, 'ファイルリストの取得', time_start, logger)
    
    # ファイルの仕分け
    get_old_pictures(files, size_max)
    rec_time(time_dic, 'ファイルの仕分け', time_start, logger)
    
    # ファイル移動関係は、エラー時もログファイルを出力する
    try:        
        # ファイルの絞り込み
        info_dic['全ファイル数'] = '{}(files)'.format(len(files))
        files = list(filter(lambda x: x.allow_copy, files))
        info_dic['対象ファイル数'] = '{}(files)'.format(len(files))
        rec_time(time_dic, '転送準備', time_start, logger)

        # 特定したファイルをファイル転送
        move_files(files, backup_dir, logger)
        rec_time(time_dic, 'ファイル転送', time_start, logger)

        # GIFのコピーを作る（GIFアニメーション用）
        out_gifs, png_files = save_to_gif(backup_dir, gif_dir, thumb_max)
        rec_time(time_dic, 'GIFコピー', time_start, logger)

        # GIFアニメーションを作成する
        dul_ms = int(ini_data['picture']['dulation_ms'])
        make_gif_animation(out_gifs, output_dir, now_str, thumb_max, dul_ms)
        rec_time(time_dic, 'GIFアニメーションの作成', time_start, logger)

        # 一時フォルダをzip化する

        # zipファイルをDドライブの専用フォルダへ移動する
    except Exception as ex:
        logger.logger.error(ex)
        print(ex)
    finally:
        time_dic['処理開始'] = 0

        # ログファイルの出力
        csv_sub = ini_data['log']['csv']
        file_latest = max([ti.create_time for ti in files])
        file_sum = int(sum([si.file_size for si in files]))
        info_dic['対象ファイルの最終日時'] =  file_attr.get_datetime_str(file_latest, '%Y/%m/%d %H:%M:%S')
        info_dic['対象ファイルの総サイズ'] =  '{:.1f}(MB)'.format(file_attr.get_size_str(file_sum, 'MB'))

    try:
        output_csv_log(files, output_dir, csv_sub)
        output_logger(logger, info_dic, time_dic)
    except Exception as ex:
        logger.error('!!ログ出力エラー', ex)
    print('finished')

if __name__ == '__main__':
    main()