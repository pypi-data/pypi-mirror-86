# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import *
import os
import sys
import traceback

from . import setup_it

USAGE = '''
Usage: python -m setupmeta_builder [OPTIONS] COMMAND [ARGS]...

Options:
  --

Commands:
  setup                 equals `python setup.py` with setupmeta_builder proxy
  create-setup.py       create `setup.py`
  print                 print resolved attrs
'''.strip()

def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = argv[1:]
    try:
        if not args:
            print(USAGE)
        elif args[0] == 'setup':
            setup_it()
        elif args[0] == 'create-setup.py':
            from .cli.make_setup import create_setup_py
            create_setup_py((args + [None])[1])
        elif args[0] == 'print':
            from .cli.print_attrs import print_setup_attrs
            print_setup_attrs((args + [None])[1])
        else:
            print(USAGE)
    except Exception:
        traceback.print_exc()

if __name__ == '__main__':
    main()
