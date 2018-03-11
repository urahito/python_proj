# -- coding: utf-8 --
from pathlib import Path
import time

class file_attr:    
    def __init__(self, fpath, ctime, fsize, dest_dir):
        org_path = Path(fpath)
        self.org_path = org_path
        self.create_time = ctime
        self.file_size = fsize
        self.dest_path = Path(dest_dir) / org_path.name

    def __str__(self):
        org_name = self.org_path.name        
        return "[{}]({}),{},{},[{}]({})" \
            .format(org_name, \
                    self.org_path, \
                    time.localtime(self.create_time), \
                    self.file_size, \
                    self.dest_path.parent, \
                    self.dest_path)
