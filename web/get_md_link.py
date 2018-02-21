# coding: utf-8

import sys, bs4, requests, csv, os, codecs
import unicodedata
from pathlib import Path

def main():
    # 親ディレクトリの取得
    parent_dir = Path(__file__).parent

    # 入力、出力ファイル・ディレクトリの取得
    files = list(parent_dir.joinpath('org').glob('*.txt'))
    out_file = codecs.open(parent_dir.joinpath('out/result.csv'), 'w', 'sjis')
    out_writer = csv.writer(out_file, dialect="excel")

    # 入力ファイルでfor文を回す
    for file_path in files:
        # 指定ファイルをutf-8で開く
        file_obj = open(file_path, 'r', encoding='utf-8')
        # 全行取り込む
        url_list = file_obj.readlines()

        # urlリストを1行ごとに処理する
        for url in url_list:
            url = url.replace('\r', '').replace('\n', '')

            # ページの取得
            res = requests.get(url)
            soup = bs4.BeautifulSoup(res.text)

            # タイトルの取得とMarkdown用フォーマット
            title = soup.select('title')[0].getText().encode('sjis', 'ignore').decode('sjis')
            markup = '[{}]({})'.format(title, url)

            # csvファイルへ書き出し
            out_writer.writerow([url, title, markup])

if __name__ == '__main__':
    main()