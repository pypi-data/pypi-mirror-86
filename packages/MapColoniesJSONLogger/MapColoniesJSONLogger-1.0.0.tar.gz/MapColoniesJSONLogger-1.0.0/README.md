# json-logger

## Installation
```
pip3 install mapcoloniesjsonlogger
```

## Usage Example
```py
from MapColoniesJSONLogger.logger import generate_logger
import os

log = generate_logger('service_name', log_level='INFO', handlers=[{'type': 'rotating_file', 'path': '/var/log/service.log'}])
log.info('basic message')
log.info('message with extra fields', extra={'extra.field': 'extra_value', 'service': 'some_service'}) # supports nesting of fields
log.debug('will not be in a file')
```

## Configuration Example
The configuration dict bellow is used by the package. For more information on logging configuration see [logging.config](https://docs.python.org/3.6/library/logging.config.html#module-logging.config) docs
