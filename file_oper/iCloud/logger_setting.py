import logging
from pathlib import Path

class logger_setting:
    def __init__(self, ini_data, name, now_str):
        log_dir = Path(ini_data['settings']['output']) / ini_data['log']['logging'] 
        self.log_path = log_dir / 'log-{}.log'.format(now_str)
        Path(log_dir).mkdir(exist_ok=True)

        datefmt='%Y/%m/%d %H:%M:%S'
        fmt = '[%(asctime)s] %(module)s.%(funcName)s %(levelname)s -> %(message)s'
        logging.basicConfig(filename = self.log_path, level = logging.INFO, format=fmt, datefmt=datefmt)        
        self.logger = logging.getLogger(name)

    def get_logger(self):
        return self.logger
    
    def info(self, msg):
        self.logger.info(msg)
    
    def debug(self, msg):
        self.logger.debug(msg)
    
    def warn(self, msg):
        self.logger.warn(msg)
    
    def error(self, msg, ex):
        self.logger.error(msg, exc_info=True)
    
    def critical(self, msg, ex):
        self.logger.critical(msg, exc_info=True)
