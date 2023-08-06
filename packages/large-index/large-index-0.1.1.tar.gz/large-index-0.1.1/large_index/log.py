#!/usr/bin/python3

import sys
import logging
from os import path, remove

class Log:
  def __init__(self,
  ):
    super().__init__()
    self.logger = logging.getLogger(__name__)
    self.log_file_format = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')

  def get_file_handler(self):
    self.file_handler = logging.FileHandler('large_index.log')
    self.file_handler.setFormatter(self.log_file_format)

  def get_stream_handler(self):
    self.stream_handler = logging.StreamHandler()
    self.stream_handler.setFormatter(self.log_file_format)

  def get_logger(self):
    self.logger.setLevel(logging.INFO)
    self.logger.addHandler(self.file_handler)
    self.logger.addHandler(self.stream_handler)

  def remove_old_log_file(self):
    if path.isfile('large_index.log'):
      remove('large_index.log')

if __name__ == "__main__":
  class_log = Log()
  class_log.remove_old_log_file()
  class_log.get_file_handler()
  class_log.get_stream_handler()
  class_log.get_logger()
