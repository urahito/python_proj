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
        self.create_time = ctime
        self.file_size = fsize
        self.dest_path = Path(dest_dir) / org_path.name
        self.allow_copy = False
    
    def allow_file_copy(self, size_max):
        if (self.org_path.exists() and self.org_path.is_file()) == False:
            return
        elif self.file_size <= 0:
            return
        elif size_max + self.file_size > 500 * (1024 ** 2):
            return
        self.allow_copy =  True
        return size_max + self.file_size

    def get_file_info(self):
        print('')

    def __str__(self):
        org_name = self.org_path.name     
        create_str = datetime.datetime.fromtimestamp(self.create_time).strftime('%Y/%m/%d %H:%M:%S') 

        return "[{}]({}),{},{},[{}]({})" \
            .format(org_name, \
                    self.org_path, \
                    create_str, \
                    self.file_size, \
                    self.dest_path.parent, \
                    self.dest_path)