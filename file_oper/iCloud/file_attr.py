# -- coding: utf-8 --
from pathlib import Path
import datetime, os

class file_attr:    
    def __init__(self, fpath, dest_dir):
        org_path = Path(fpath)
        if (org_path.exists() == False):
            return

        ctime = os.path.getmtime(org_path)
        fsize = os.path.getsize(org_path)

        self.org_path = org_path
        self.create_time = datetime.datetime.fromtimestamp(ctime)
        self.file_size = fsize
        self.dest_path = Path(dest_dir) / org_path.name
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

    def get_file_info(self):
        print('')

    def __str__(self):
        org_name = self.org_path.name     
        create_str = self.create_time.strftime('%Y/%m/%d %H:%M:%S') 

        return "[{}]({}),{},{},[{}]({}),{}" \
            .format(org_name, \
                    self.org_path, \
                    create_str, \
                    self.file_size, \
                    self.dest_path.parent, \
                    self.dest_path, \
                    self.allow_copy)