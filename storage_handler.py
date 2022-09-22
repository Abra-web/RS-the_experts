from os.path import basename, dirname, abspath, join, exists, relpath, isfile
from os import makedirs, getenv, listdir
import re
import logging
import sys
from datetime import date, datetime

# Windows path fix, if system is windows then it replaces the forward slashes for the regex statement later
"""
Purpose of script:
a)  Define directory paths
"""

# local data folder structure
DIR_ROOT = dirname(abspath(__file__))
DIR_DATA = join(DIR_ROOT, 'data')
DIR_DATA_JSON=join(DIR_DATA,'json')
DIR_DATA_CSV=join(DIR_DATA,'csv')


class Storage:
    def __init__(self):

        self._setup()

    def _setup(self):
        # create local data folder structure, if it doesn't exist yet
        for d in [DIR_DATA,DIR_DATA_JSON,DIR_DATA_CSV]:
            makedirs(d, exist_ok=True)
        print('Storage set up.')

