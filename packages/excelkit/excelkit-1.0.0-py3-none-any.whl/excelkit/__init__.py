#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""

"""
import os
import sys
import json
import warnings


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
version_info = json.load(open(os.path.join(BASE_DIR, 'version', 'version.json')))

PY2 = sys.version_info.major == 2
if PY2:
    reload(sys) 
    sys.setdefaultencoding('utf-8')

warnings.filterwarnings('ignore')
