import logging, logging.config, time
from os import path
import copy
from pythonjsonlogger import jsonlogger

from jsonlogger.default_config import default_config


def merge(a: dict, b: dict):
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key])
            elif a[key] == b[key]:
                pass
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a


def JSONLogger(name: str, config: dict = {}, additional_fields: dict = None):
    """
    Constructor that creates a logger instance (wrapped by an adapter)

    Args:
        name (str): name to associate with the logger
        config (dict, optional): logging configuration
        additional_fields (dict, optional): dict of additional key/value pairs to log. Defaults to None.
    """
    if len(name) == 0:
        raise Exception('Name of the logger must be present')
    merged_config = copy.deepcopy(default_config)
    merged_config = merge(merged_config, config)
    logging.config.dictConfig(merged_config)
    # create logger and save it
    return CustomLoggerAdapter(logging.getLogger(name), additional_fields)


class CustomLoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger, additional_fields):
        super(CustomLoggerAdapter, self).__init__(logger, {})
        self.additional_fields = additional_fields

    def process(self, msg, kwargs):
        extra = self.extra.copy()
        extra.update(kwargs.get('extra', dict()))
        if self.additional_fields: extra.update(self.additional_fields)
        kwargs['extra'] = extra
        return msg, kwargs


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # combine time with milliseconds to form a timestamp
            log_record['timestamp'] = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(record.created)) + f'.{round(record.msecs):03d}'
        if log_record.get('loglevel'):
            log_record['loglevel'] = log_record['loglevel'].upper()
        else:
            log_record['loglevel'] = record.levelname
