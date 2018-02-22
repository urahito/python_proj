# coding: utf-8

import csv # ファイル出力用
import bs4, requests # スクレイピング(html取得・処理)
import re #正規表現
from pathlib import Path

# 指定エンコードのgetメソッド
def get_enc(mode):
    enc_dic = dict(r='utf-8', w='sjis', p='cp932')
    return enc_dic[mode]

# インラインのfor文リストで除外文字以外を繋ぐ
def remove_str(target, str_list):    
    return ''.join([c for c in target if c not in str_list])

# 指定エンコードでエラー文字以外を再取得する
def ignore_str(target, enc):    
    return target.encode(enc, 'ignore').decode(enc)

# urlからタイトルを取得し、csvファイルに出力する
def read_url(url_list, out_writer):
        # urlリストを1行ごとに処理する
        for url in url_list:
            url = remove_str(url, ['\r', '\n'])

            # 正規表現処理
            rep = r'^https?://[\w/:%#\$&\?\(\)~\.=\+\-]+$'
            isUrl = re.match(rep, url) != None

            # urlでなければ次へ
            if not isUrl:
                print('{} do not matched url pattern'.format(url))
                continue

            # ページの取得
            res = requests.get(url)
            soup = bs4.BeautifulSoup(res.text)

            # タイトルの取得とMarkdown用フォーマット
            title = ignore_str(soup.title.string, get_enc('w'))
            markup = '[{}]({})'.format(title, url)

            # csvファイルへ書き出し
            out_writer.writerow([url, title, markup])

def main():
    # 各ディレクトリの取得
    parent_dir = Path(__file__).parent
    org_dir = parent_dir / 'org'
    out_dir = parent_dir / 'out'

    # フォルダが無ければ作成（あってもエラーなし）
    org_dir.mkdir(exist_ok=True)
    out_dir.mkdir(exist_ok=True)

    # 出力ファイルの決定
    out_file = out_dir / 'result.csv'

    # 入力、出力ファイル・ディレクトリの取得
    files = list(org_dir.glob('*.txt'))
    with out_file.open('w', encoding=get_enc('w'), newline='') as out_file_obj:
        # csvファイルのwriterを取得
        out_writer = csv.writer(out_file_obj, dialect="excel")

        # 入力ファイルでfor文を回す
        for file_path in files:
            with Path(file_path).open('r', encoding=get_enc('r')) as read_file_obj:
                # 全行取り込む
                url_list = read_file_obj.readlines()

                # urlの読み込み
                read_url(url_list, out_writer)

if __name__ == '__main__':
    main()