# coding: utf-8

import sys, bs4, requests, csv, os, codecs
import unicodedata
from pathlib import Path

def remove_str(target, str_list):
    return ''.join([c for c in target if c not in str_list])

def ignore_str(target, enc):
    return target.encode(enc, 'ignore').decode(enc)

def read_url(url_list, out_writer):
        # urlリストを1行ごとに処理する
        for url in url_list:
            url = remove_str(url, ['\r', '\n'])

            # ページの取得
            res = requests.get(url)
            soup = bs4.BeautifulSoup(res.text)

            # タイトルの取得とMarkdown用フォーマット
            title = ignore_str(soup.title.string, 'sjis')
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
    out_file = out_dir / 'result.csv'

    # 入力、出力ファイル・ディレクトリの取得
    files = list(org_dir.glob('*.txt'))
    with out_file.open('w', encoding='utf-8', newline='') as out_file_obj:
        out_writer = csv.writer(out_file_obj, dialect="excel")

        # 入力ファイルでfor文を回す
        for file_path in files:
            with Path(file_path).open('r', encoding='utf-8') as file_obj:
                # 全行取り込む
                url_list = file_obj.readlines()

                read_url(url_list, out_writer)

if __name__ == '__main__':
    main()