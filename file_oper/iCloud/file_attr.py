# -- coding: utf-8 --
from pathlib import Path
import datetime

class file_attr:    
    def __init__(self, fpath, ctime, fsize, dest_dir):
        org_path = Path(fpath)
        self.org_path = org_path
        self.create_time = ctime
        self.file_size = fsize
        self.dest_path = Path(dest_dir) / org_path.name

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