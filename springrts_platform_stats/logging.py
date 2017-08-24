# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging.handlers
from django.conf import settings


handler_name = 'spslog'
level = getattr(logging, settings.MY_LOGGING['level'], logging.INFO)
logger = logging.getLogger('sps')
logger.setLevel(max(logger.level, level))
if handler_name not in [h.name for h in logger.handlers]:
    _file_handler = logging.handlers.TimedRotatingFileHandler(
        settings.MY_LOGGING['logfile'], when='W0', interval=1, backupCount=52)
    _file_handler.name = handler_name
    _formatter = logging.Formatter(datefmt=settings.MY_LOGGING['datefmt'], fmt=settings.MY_LOGGING['msg_format'])
    _file_handler.setFormatter(_formatter)
    _file_handler.setLevel(level)
    logger.addHandler(_file_handler)
