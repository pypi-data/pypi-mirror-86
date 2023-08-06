#!/usr/bin/python3

import click
import logging

from large_index.log import Log
from large_index.config import Config
from large_index.init import Init
from large_index.structure import Structure

class_config = Config
class_structure = Structure()
class_log = Log()

class_log.remove_old_log_file()
class_log.get_file_handler()
class_log.get_stream_handler()
class_log.get_logger()

def logging_level(level):
  if level:
    logging_level_critical(level)
    logging_level_error(level)
    logging_level_warning(level)
    logging_level_info(level)
    logging_level_debug(level)
    logging_level_notset(level)

def logging_level_critical(level):
  if level == 'critical' or level == 'CRITICAL' or level == '=critical' or level == '=CRITICAL':
    class_log.logger.setLevel(logging.CRITICAL)

def logging_level_error(level):
  if level == 'error' or level == 'ERROR' or level == '=error' or level == '=ERROR':
    class_log.logger.setLevel(logging.ERROR)

def logging_level_warning(level):
    if level == 'warning' or level == 'WARNING' or level == '=warning' or level == '=WARNING':
      class_log.logger.setLevel(logging.WARNING)

def logging_level_info(level):
    if level == 'info' or level == 'INFO' or level == '=info' or level == '=INFO':
      class_log.logger.setLevel(logging.INFO)

def logging_level_debug(level):
    if level == 'debug' or level == 'DEBUG' or level == '=debug' or level == '=DEBUG':
      class_log.logger.setLevel(logging.DEBUG)

def logging_level_notset(level):
    if level == 'notset' or level == 'NOTSET' or level == '=notset' or level == '=NOTSET':
      class_log.logger.setLevel(logging.NOTSET)

def generating_variables():
  class_config.index_pools = Init(count = 4).list_pools()
  class_config.ilm_list = class_config.index_pools[3].json()
  class_config.settings_list = class_config.index_pools[2].json()
  class_config.alias_list = class_config.index_pools[1].json()

  class_structure.logger = class_log.logger

  class_structure.create_array_index_details_in_open()
  class_structure.create_array_index_to_remove()
  class_structure.remove_system_index_in_array()
  class_structure.create_array_indices()
  class_structure.create_array_max_indices()

  del(class_structure.index_details)
  del(class_structure.index_to_remove)

  class_structure.create_array_invalid_size_index()
  class_structure.remove_invalid_data_in_index( class_structure.invalid_size_indices )

  class_structure.create_array_unmanaged_index()
  class_structure.remove_invalid_data_in_index( class_structure.unmanaged_indices )

  class_structure.create_array_not_hot_box_index()
  class_structure.remove_invalid_data_in_index( class_structure.not_hot_box_indices )

  class_structure.create_array_not_hot_phase_index()
  class_structure.remove_invalid_data_in_index( class_structure.not_hot_phase_indices )

  class_structure.create_array_shrink_index()
  class_structure.remove_invalid_data_in_index( class_structure.shrink_indices )

  class_structure.create_last_index()
  class_structure.create_not_last_index()
  class_structure.create_last_shrink_index()

  del(class_structure.invalid_size_indices)
  del(class_structure.unmanaged_indices)
  del(class_structure.not_hot_box_indices)
  del(class_structure.not_hot_phase_indices)

def start_rollover_all(check_mode):
  if not check_mode:
    class_structure.rollover_last_index()
    class_structure.rollover_not_last_index()
    class_structure.rollover_last_shrink_index()

def start_check_mode_rollover_all(check_mode):
  if check_mode:
    class_structure.rollover_last_index_in_check_mode()
    class_structure.rollover_not_last_index_in_check_mode()
    class_structure.rollover_last_shrink_index_in_check_mode()

def start_rollover_last_index(check_mode):
  if not check_mode:
    class_structure.rollover_last_index()

def start_check_mode_rollover_last_index(check_mode):
  if check_mode:
    class_structure.rollover_last_index_in_check_mode()

def start_rollover_not_last_index(check_mode):
  if not check_mode:
    class_structure.rollover_not_last_index()

def start_check_mode_rollover_not_last_index(check_mode):
  if check_mode:
    class_structure.rollover_not_last_index_in_check_mode()

def start_rollover_last_shrink_indices(check_mode):
  if not check_mode:
    class_structure.rollover_last_shrink_index()

def start_check_mode_rollover_last_shrink_indices(check_mode):
  if check_mode:
    class_structure.rollover_last_shrink_index_in_check_mode()

@click.group()
@click.version_option()
def cli():
  """
  Rollover big indexes ilm in Elasticsearch.
  """
  pass

@cli.command(help='Rollover large indexes.')
@click.option(
  '-c', '--check-mode',
  is_flag=True,
  expose_value=True,
  help='Only displaying actions, without performing them.'
)
@click.option(
  '-l', '--log-level',
  default='info',
  show_default=False,
  expose_value=True,
  help='The output level of logs. \n\nOptions: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL'
)
def start(check_mode, log_level):
  """
  Rollover large indexes.
  """
  logging_level(log_level)
  class_log.logger.info("Started rollover large indexes")

  generating_variables()
  start_rollover_all(check_mode)
  start_check_mode_rollover_all(check_mode)

@cli.command(help='Rollover only the latest big indexes (not shrink).')
@click.option(
  '-c', '--check_mode',
  is_flag=True,
  expose_value=True,
  help='Only displaying actions, without performing them.'
)
@click.option(
  '-l', '--log-level',
  default='info',
  show_default=False,
  expose_value=True,
  help='The output level of logs. \n\nOptions: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL'
)
def last_index(check_mode, log_level):
  """
  Rollover only the latest big indexes (not shrink index).
  """
  logging_level(log_level)
  class_log.logger.info("Started rollover only the latest big indexes (not shrink index).")

  generating_variables()
  start_rollover_last_index(check_mode)
  start_check_mode_rollover_last_index(check_mode)

@cli.command(help='Rollover only the not latest big indexes (not shrink).')
@click.option(
  '-c', '--check_mode',
  is_flag=True,
  expose_value=True,
  help='Only displaying actions, without performing them.'
)
@click.option(
  '-l', '--log-level',
  default='info',
  show_default=False,
  expose_value=True,
  help='The output level of logs. \n\nOptions: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL'
)
def not_last_index(check_mode, log_level):
  """
  Rollover only the not latest big indexes (not shrink index).
  """
  logging_level(log_level)
  class_log.logger.info("Started rollover only the not latest big indexes (not shrink index)")

  generating_variables()
  start_rollover_not_last_index(check_mode)
  start_check_mode_rollover_not_last_index(check_mode)

@cli.command(help='Rollover only the latest big shrink indexes.')
@click.option(
  '-c', '--check_mode',
  is_flag=True,
  expose_value=True,
  help='Only displaying actions, without performing them.'
)
@click.option(
  '-l', '--log-level',
  default='info',
  show_default=False,
  expose_value=True,
  help='The output level of logs. \n\nOptions: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL'
)
def last_shrink_index(check_mode, log_level):
  """
  Rollover only the latest big shrink indexes.
  """
  logging_level(log_level)
  class_log.logger.info("Started rollover only the latest big shrink indexes")

  generating_variables()
  start_rollover_last_shrink_indices(check_mode)
  start_check_mode_rollover_last_shrink_indices(check_mode)

if __name__ == "__main__":
  cli()
