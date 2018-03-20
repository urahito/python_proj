import logging

class logger_setting:
    def __init__(self, ini_data):
        self.log_path = ini_data['log']['logging']
        logging.basicConfig(filename = self.log_path, level = logging.INFO,
                       format='[%(asctime)s] %(module)s.%(funcName)s %(levelname)s -> %(message)s')
        self.logger = logging.getLogger(__name__)

    def Info(self, msg):
        logging.info(msg)

    def Debug(self, msg):
        logging.debug(msg)

    def Warn(self, msg):
        logging.warn(msg)

    def Error(self, msg):
        logging.error(msg)
    
    def Critical(self, msg):
        logging.critical(msg)
