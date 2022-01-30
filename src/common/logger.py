import logging
from datetime import datetime

class LogFormatter(logging.Formatter):

    def __init__(self, attr, **kwargs):
        super().__init__(**kwargs)
        self._attr = attr

    def format(self, record: logging.LogRecord):
        _record = {
            attr_name: record.__dict__[attr_name]
            for attr_name in record.__dict__
            if attr_name in self._attr
        }

        _record['message'] = record.getMessage()

        # Customize timestamp (isoformat not available with 'asctime')
        _record['timestamp'] = datetime.now().isoformat(timespec='milliseconds')

        # Rename 'levelname' key to 'level' for consistency with the other components
        _record['level'] = _record['levelname'].lower()
        del _record['levelname']

        if getattr(record, 'exc_info', None) is not None:
            _record['exc_info'] = self.formatException(record.exc_info)

        _record['message'] = _record.get('exc_info', _record['message'])
        return '{timestamp} - {level: <8} - {name} - "{message}"'.format(**_record)


def logging_setup(name):
    logger = logging.getLogger(name)

    # Text Formatter
    formatter = LogFormatter(
        attr=['time', 'levelname', 'message', 'name']
    )

    # Output logs in stdout
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel('INFO')

    logging.getLogger('werkzeug').disabled = True

    return logger


# Override default sqlalchemy logger
logger = logging_setup('allisone')
