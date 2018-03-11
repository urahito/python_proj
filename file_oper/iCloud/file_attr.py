# -- coding: utf-8 --
from pathlib import Path
import datetime, os

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
    
    def __init__(self, fpath, dest_dir):
        org_path = Path(fpath)
        if (org_path.exists() == False):
            return

        ctime = os.path.getmtime(org_path)
        fsize = os.path.getsize(org_path)

        self.org_path = org_path
        self.create_time = datetime.datetime.fromtimestamp(ctime)
        self.file_size = fsize
        self.dest_org = Path(dest_dir)
        self.dest_path = self.dest_org / org_path.name
        self.allow_copy = False
    
    # 有効なファイルかどうか
    def is_file(self):
        # 存在するファイルであること
        result = self.org_path.exists() and self.org_path.is_file()
        # ファイルサイズがあること
        result = result and (self.file_size > 0)
        return result
    
    # 対象の日付か
    def is_target_day(self, days_before):
        today = datetime.datetime.today()
        th_date = today - datetime.timedelta(days=days_before)
        return self.create_time < th_date
    
    # 対象ファイルチェック
    def allow_file_copy(self, sum_size, size_max, days_before, past_ng):
        ng_result = (sum_size, True)
        ok_result = ((sum_size + self.file_size), False)
        is_over_size = sum_size + self.file_size > size_max

        '''
        【チェック内容】
        1. 既にNGが出ていないこと
        2. 有効なファイルか
        3. 90日前までに作成されていること
        4. ファイルサイズの累計が上限値を超えないこと
        '''        
        result = past_ng == False                        
        result = result and self.is_file()   
        result = result and self.is_target_day(days_before)
        result = result and is_over_size == False                

        if result == False:
            return ng_result
        
        self.allow_copy =  True
        return ok_result
    
    def set_sub_dir(self, sub_dir):
        self.dest_path = self.dest_org / sub_dir / self.org_path.name

    def output_line(self):
        org_name = self.ignore_str(str(self.org_path.name), self.get_enc('w'))  
        dest_dir = self.ignore_str(str(self.dest_path.parent), self.get_enc('w'))  
        create_str = self.create_time.strftime('%Y/%m/%d %H:%M:%S') 
        size_str = str(int(self.get_size_str(self.file_size, 'KB')))

        return [org_name, create_str, size_str, dest_dir, self.allow_copy]

    def __str__(self):
        org_name = self.org_path.name    
        create_str = self.create_time.strftime('%Y/%m/%d %H:%M:%S') 
        size_str = str(int(self.get_size_str(self.file_size, 'KB')))

        return "{},{},{},{},{}" \
            .format(org_name, \
                    create_str, \
                    size_str, \
                    self.allow_copy, \
                    self.dest_path.parent)