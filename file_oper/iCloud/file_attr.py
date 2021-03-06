# -- coding: utf-8 --
from pathlib import Path
from datetime import datetime as ddt
from datetime import timedelta as dlt
import os

class file_attr:    
    @staticmethod
    def get_big_size(value, unit):
        unit_dic = dict(B=0, KB=1, MB=2, GB=3)
        return value * (1024 ** unit_dic[unit])
    
    @staticmethod
    def get_size_str(value, unit):
        unit_dic = dict(B=0, KB=1, MB=2, GB=3)
        return value / (1024 ** unit_dic[unit])  

    # 指定エンコードのgetメソッド
    @staticmethod
    def get_enc(mode):
        enc_dic = dict(r='utf-8', w='sjis', p='cp932')
        return enc_dic[mode]

    # 指定エンコードでエラー文字以外を再取得する
    @staticmethod
    def ignore_str(target, enc):    
        return target.encode(enc, 'ignore').decode(enc)  
    
    # 外部用datetimeのstr取得メソッド
    @staticmethod
    def get_datetime_str(value, format):
        return value.strftime(format)

    # datetimeのstr取得メソッド
    def get_createtime_str(self):
        return self.get_datetime_str(self.create_time, '%Y/%m/%d %H:%M:%S')
    
    @staticmethod
    def make_parent_dir(path_obj, sub_dir=''):
        path_sub = path_obj / sub_dir
        results = {}
        results['parent_exist'] = path_obj.exists()
        results['sub_exist'] = path_sub.exists()        
        #results['is_file'] = path_sub.exists()

        if results['parent_exist']:            
            if not results['sub_exist']:
                path_sub.mkdir(exist_ok=True)
            path_obj = path_sub
        else: 
            path_sub.mkdir(exist_ok=True)
            path_obj = path_sub
        return path_obj

    def __init__(self, fpath, dest_dir):
        org_path = Path(fpath)
        if not org_path.exists():
            return

        ctime = org_path.stat().st_ctime
        fsize = org_path.stat().st_size

        self.org_path = org_path
        self.create_time = ddt.fromtimestamp(ctime)
        self.file_size = fsize
        self.dest_org = Path(dest_dir)
        self.dest_path = self.dest_org / org_path.name
        self.allow_copy = False
    
    # 有効なファイルかどうか(all(list(bool))で判定)
    def is_file(self): 
        results = []
        results.append(self.org_path.exists())
        results.append(self.org_path.is_file())
        results.append(self.file_size > 0) 
        return all(results)
    
    # 対象の日付か
    def is_target_day(self, days_before):
        today = ddt.today()
        th_date = today - dlt(days=days_before)
        return self.create_time < th_date
    
    # 対象ファイルチェック
    def allow_file_copy(self, days_before, past_ng):    
        # チェック内容をdictとして記述（ログ用）
        checks = {}
        checks['past_ng_check'] = (not past_ng)
        checks['valid_file_check'] = (self.is_file())
        checks['days_range_check'] = (self.is_target_day(days_before))

        # 結果のみ取り出し
        results = list(checks.values())

        # すべてTrueでなければ対象外
        if all(results) == False:
            return self.file_size
        
        self.allow_copy =  True
        return self.file_size
    
    def set_sub_dir(self, sub_dir):
        self.dest_path = self.dest_org / sub_dir / self.org_path.name

    def output_line(self):
        org_name = self.ignore_str(str(self.org_path.name), self.get_enc('w'))  
        dest_dir = self.ignore_str(str(self.dest_path.parent), self.get_enc('w'))  
        create_str = self.get_createtime_str() 
        size_str = str(int(self.get_size_str(self.file_size, 'KB')))

        return [org_name, create_str, size_str, dest_dir, self.allow_copy]

    def __str__(self):
        org_name = self.org_path.name    
        create_str = self.get_createtime_str()
        size_str = str(int(self.get_size_str(self.file_size, 'KB')))

        return "{},{},{},{},{}" \
            .format(org_name, \
                    create_str, \
                    size_str, \
                    self.allow_copy, \
                    self.dest_path.parent)