import logging, logging.config, time
from logging import LoggerAdapter
from os import path
from typing import List
import copy
import sys

import ecs_logging

def get_stream_handler(config: dict):
    available_options = {
        'stdout': sys.stdout,
        'stderr': sys.stderr
    }
    if config['output'] not in available_options.keys:
        raise ValueError('output type {0} passed but is not an accepted value, available options: {1}'.format(config['output'], ' '.join(available_options.keys())))
    return logging.StreamHandler(stream=available_options[config['output']])

def get_rotating_file_handler(config: dict):
    if not config['path']:
        raise ValueError('file path must not be empty')
    if not path.exists(path.dirname(config['path'])):
        raise ValueError('path must exist')
    return logging.handlers.RotatingFileHandler(filename=config['path'], maxBytes=5242880, backupCount=10, encoding='utf-8')
    
    

def generate_logger(name: str, log_level: str = 'error', handlers: List[dict] = [ { type: 'stream', output: 'stderr' } ], metadata: dict = {}):
    if not name:
        raise ValueError('name must not be empty')
    if not log_level:
        raise ValueError('log_level must not be empty')
    if len(handlers) == 0:
        raise ValueError('handlers must not be empty')
    logger = logging.getLogger(name)
    for handler_config in handlers:
        logging_handler = None
        if handler_config['type'] == 'stream':
            logging_handler = get_stream_handler(config=handler_config)
        elif handler_config['type'] == 'rotating_file':
            logging_handler = get_rotating_file_handler(config=handler_config)
        else:
            raise ValueError('unsupported handler type')
        logging_handler.setFormatter(ecs_logging.StdlibFormatter)
        logger.addHandler(logging_handler)
    logger.setLevel(log_level)
    return LoggerAdapter(logger, metadata)
