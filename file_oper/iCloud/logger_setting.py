import logging
from pathlib import Path

class logger_setting:
    def __init__(self, ini_data, logger):
        log_dir = Path(ini_data['settings']['output']) / ini_data['log']['logging'] 
        self.log_path = log_dir / 'log.log'
        Path(log_dir).mkdir(exist_ok=True)
        logging.basicConfig(filename = self.log_path, level = logging.INFO,
                       format='[%(asctime)s] %(module)s.%(funcName)s %(levelname)s -> %(message)s')
        self.logger = logger
