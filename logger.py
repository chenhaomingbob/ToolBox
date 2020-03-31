#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/03/23
    Description:
"""
import datetime
import logging

import termcolor

# from __init__ import __appname__

__appname__ = "chenhaomingbob_ToolBox"
COLORS = {
    'WARNING': 'yellow',
    'INFO': 'white',
    'DEBUG': 'blue',
    'CRITICAL': 'red',
    'ERROR': 'red',
}


class ColoredFormatter(logging.Formatter):

    def __init__(self, fmt, use_color=True):
        logging.Formatter.__init__(self, fmt)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            def colored(text):
                return termcolor.colored(
                    text,
                    color=COLORS[levelname],
                    attrs={'bold': True},
                )

            record.levelname2 = colored('{:<7}'.format(record.levelname))
            record.message2 = colored(record.msg)

            asctime2 = datetime.datetime.fromtimestamp(record.created)
            record.asctime2 = termcolor.colored(asctime2, color='green')

            record.module2 = termcolor.colored(record.module, color='cyan')
            record.funcName2 = termcolor.colored(record.funcName, color='cyan')
            record.lineno2 = termcolor.colored(record.lineno, color='cyan')
        return logging.Formatter.format(self, record)


class ColoredLogger(logging.Logger):
    FORMAT = (
        '[%(levelname2)s] %(module2)s:%(funcName2)s:%(lineno2)s - %(message2)s'
    )

    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.INFO)

        color_formatter = ColoredFormatter(self.FORMAT)

        console = logging.StreamHandler()
        console.setFormatter(color_formatter)

        self.addHandler(console)
        return


logging.setLoggerClass(ColoredLogger)
logger = logging.getLogger(__appname__)
