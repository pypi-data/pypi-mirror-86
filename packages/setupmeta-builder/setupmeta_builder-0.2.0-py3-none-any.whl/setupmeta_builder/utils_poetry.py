# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import *
import re

from packaging.requirements import Requirement
try:
    from poetry.core.semver import parse_constraint
except ModuleNotFoundError:
    from poetry.semver import parse_constraint

RE_AUTHORS = re.compile('^(?P<name>.+) <(?P<email>.+@.+)>$')

def parse_author(author: str) -> Tuple[str, str]:
    author = author.strip()
    match = RE_AUTHORS.match(author)
    if match:
        author_name, author_email = match.group('name'), match.group('email')
        return author_name, author_email
    return author, None

def get_requirements(items: dict, inculde_optional) -> Dict[str, Requirement]:
    rv = {}
    for k, v in items.items():
        vc = None

        if isinstance(v, str):
            vc = parse_constraint(v)

        elif isinstance(v, dict):
            if not v.get('optional') or inculde_optional:
                version = v.get('version')
                if isinstance(version, str):
                    vc = parse_constraint(version)

        else:
            raise NotImplementedError(type(v))

        if vc:
            vcs = str(vc)
            if vcs == '*':
                rv[k] = Requirement(k)
            else:
                rv[k] = Requirement(k + vcs)

    return rv
