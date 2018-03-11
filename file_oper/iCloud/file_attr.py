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
    
    def allow_file_copy(self, sum_size, size_max):
        # 存在するファイルであること
        if (self.org_path.exists() and self.org_path.is_file()) == False:
            return sum_size
        # ファイルサイズがあること
        elif self.file_size <= 0:
            return sum_size
        # 90日前までに作成されたファイルであること
        elif self.create_time >= datetime.datetime.today() - datetime.timedelta(days=90):
            return sum_size
        # ファイルサイズの累計が上限値を超えないこと
        elif sum_size + self.file_size > size_max:
            return sum_size
        
        self.allow_copy =  True
        return sum_size + self.file_size
    
    def set_sub_dir(self, sub_dir):
        self.dest_path = self.dest_org / sub_dir / self.org_path.name

    def __str__(self):
        org_name = self.org_path.name     
        create_str = self.create_time.strftime('%Y/%m/%d %H:%M:%S') 
        size_str = str(int(self.get_size_str(self.file_size, 'KB')))

        return "{},{},{},{},{}" \
            .format(org_name, \
                    create_str, \
                    size_str, \
                    self.dest_path.parent, \
                    self.allow_copy)