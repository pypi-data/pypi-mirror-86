# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import sys

from prettyprinter import pprint

from .. import get_setup_attrs

def print_setup_attrs(root_dir=None):
    root_dir = root_dir or os.getcwd()
    setup_attrs = get_setup_attrs(root_dir)
    long_description = setup_attrs['long_description']
    if long_description and len(long_description) > 205:
        setup_attrs['long_description'] = long_description[:200] + '...'
    pprint(setup_attrs)

if __name__ == '__main__':
    print_setup_attrs((sys.argv + [None])[1])
