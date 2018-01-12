import os,sys,codecs

def append_br_tag(input_path, output_path):
    # ファイル存在チェック
    if not (os.path.exists(input_path) and os.path.isfile(input_path)):
        return False

    # ファイルの読み込み
    lines = []
    try:
        input_file = codecs.open(input_path, 'r', 'utf-8')
        lines = input_file.readlines()
    except IOError as ex:
        print(ex)
        return False
    finally:
        input_file.close()

    # ファイルの書き込み
    try:
        output_file = codecs.open(output_path, 'w', 'utf-8')

        # 先に\rだけ置換するのは、Webサービスからのコピーが\r\n対応でない場合を考慮したため
        for line in lines:
            if not '<br>' in line:
                output_file.write(line.replace('\r', '').replace('\n', '<br>\r\n'))
            else:
                output_file.write(line)
    except IOError as ex:
        print(ex)
        return False
    finally:
        output_file.close()

    return True

def make_output(path):
    # ファイル存在チェック
    if not (os.path.exists(path) and os.path.isfile(path)):
        return ''

    # 拡張子チェック
    root, ext = os.path.splitext(path)
    if ext != '.txt':
        return ''

    # 出力ディレクトリ設定
    out_dir_path, file_name = os.path.split(path)    
    edited_dir = os.path.join(out_dir_path, 'edited')

    # 出力先フォルダが無ければ作る
    if not os.path.exists(edited_dir):
        os.mkdir(edited_dir)

    # 出力先ファイルのパスを結合
    out_file_path = os.path.join(edited_dir, file_name)

    print('output: ' + out_file_path)
    return out_file_path

def main():
    read_file_path = ''
    if len(sys.argv) > 1:
        read_file_path = sys.argv[1]

        # 指定ファイル、またはフォルダ内のファイルを操作する
        if not os.path.exists(read_file_path):
            return
        elif os.path.isfile(read_file_path):
            out_path = make_output(read_file_path)

            if append_br_tag(read_file_path, out_path):
                print('Succeed Output: ' + out_path)
            else:
                print('Failed Output: ' + out_path)
                
        elif os.path.isdir(read_file_path):
            for sub_dir_file in os.listdir(read_file_path):
                out_path = make_output(sub_dir_file)

                if append_br_tag(sub_dir_file, out_path):
                    print('Succeed Output: ' + out_path)
                else:
                    print('Failed Output: ' + out_path)

main()