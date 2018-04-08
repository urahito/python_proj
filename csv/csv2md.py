import csv, os
from argparse import ArgumentParser
from pathlib import Path

def get_args():
    parser = ArgumentParser(description='get input_dir, output_dir, opperation mode')
    parser.add_argument('-i', '--input', type=str, help='convert files from input folder', required=True)
    parser.add_argument('-o', '--output', type=str, help='output folder', required=True)
    parser.add_argument('-m', '--mode', type=str, help='csv (to md) or md (to csv)', default='csv')
    args = parser.parse_args()

    input_dir = args.input
    output_dir = args.output
    mode = args.mode
    return input_dir, output_dir, mode

def get_input():
    csv_ptn, md_ptn = ('*.csv', '*.md')
    input_dir, output_dir, mode = get_args()
    input_files = None
    path_input = Path(input_dir)
    path_output = Path(output_dir)

    if path_input.is_dir() == False:
        raise IOError
    elif mode == 'csv':
        input_files = path_input.glob(csv_ptn)
    elif mode == 'md':
        input_files = path_input.glob(md_ptn)
        raise NotImplementedError
    else:
        raise NotImplementedError
    path_output.mkdir(exist_ok=True)
    return input_files, path_output, mode

def read_csv(path_obj):
    with path_obj.open('r', encoding='utf-8') as fi:
        csv_reader = csv.reader(fi, dialect='excel')
        for row in csv_reader:
            yield row

def get_str_items(list_obj):
    for line in list_obj:
        for item in line:
            yield item

def pad_spaces(line, length):
    items = []
    for item in line:
        item_str = str(item)
        if item_str.isnumeric():
            items.append(item_str.rjust(length, ' '))
        else:
            items.append(item_str.ljust(length, ' '))
    return items

def format_to_md(lines):
    len_max = max([len(item) for item in get_str_items(lines)])
    str_lines = [pad_spaces(line, len_max) for line in lines]
    str_items = [f"|{'|'.join(item)}|" for item in str_lines]
    print(f'item length max: {len_max}')
    return str_items

def convert2csv(files, output_dir):
    path_files = [Path(file_obj) for file_obj in files]
    for path_obj in path_files:
        lines = [row for row in read_csv(path_obj)]
        str_lines = format_to_md(lines)
        for li in str_lines:
            print(li)

def main():
    files, output_dir, mode = get_input()
    if mode == 'csv':
        convert2csv(files, output_dir)

if __name__ == '__main__':
    main()