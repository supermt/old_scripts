import logging
import logging.config


LOGGER = logging.getLogger()

def init_log(log_file_path):
  logging.config.fileConfig(log_file_path)
