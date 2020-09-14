# Copyright (c) 2019 Alibaba-inc
# All Rights Reserved.

import logging
import os
from logging.handlers import RotatingFileHandler
from config.configuration import CONF

LOG = None


def getLogger(log_module="venus"):
    global LOG
    if not LOG:
        # level definition
        log_level = CONF.log_level.lower()
        if log_level == "debug":
            level = logging.DEBUG
        elif log_level == "info":
            level = logging.INFO
        elif log_level == "error":
            level = logging.ERROR
        else:
            level = logging.DEBUG

        # log dir.
        log_file = os.path.join(CONF.base_dir, CONF.log_file)
        if not os.path.exists(CONF.base_dir):
            try:
                os.makedirs(CONF.base_dir)
            except:
                pass

        try:
            max_bytes = int(CONF.rotate_maxbytes)
            backup = int(CONF.rotate_backups)
        except:
            max_bytes = 20*1024*1024
            backup = 1

        # logging.basicConfig(level=level,
        #                    format='[%(asctime)s] [%(levelname)s] '
        #                           '[PID:%(process)d] '
        #                           '%(filename)s:%(lineno)d  %(message)s',
        #                    datefmt=None,
        #                    filename=log_file)
        log_fmt = "[%(asctime)s] [%(levelname)s] [PID:%(process)d " \
                  "%(threadName)s] " \
                  "%(filename)s:%(lineno)d  %(message)s"
        formatter = logging.Formatter(log_fmt)
        sdk_handler = RotatingFileHandler(log_file, maxBytes=max_bytes,
                                          backupCount=backup)
        sdk_handler.setFormatter(formatter)
        LOG = logging.getLogger(log_module)
        LOG.setLevel(level)
        LOG.addHandler(sdk_handler)
    return LOG

def SetLogLevel(level):
    if level == "debug":
        LOG.setLevel(logging.DEBUG)
    elif level == "info":
        LOG.setLevel(logging.INFO)
    elif level == "error":
        LOG.setLevel(logging.ERROR)
    else:
        LOG.setLevel(logging.DEBUG)