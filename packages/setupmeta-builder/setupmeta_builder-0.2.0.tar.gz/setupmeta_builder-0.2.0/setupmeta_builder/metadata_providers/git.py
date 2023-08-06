# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import *
import subprocess
from functools import lru_cache

from ..bases import (
    BaseMetadataProvider, IContext
)

def get_git_output(ctx: IContext, argv: list) -> Optional[str]:
    gitdir = str(ctx.root_path / '.git')
    argv = ['git', f'--git-dir={gitdir}'] + argv
    proc = subprocess.run(argv,
        encoding='utf-8',
        cwd=ctx.root_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if proc.returncode == 0:
        return proc.stdout.strip()

@lru_cache(maxsize=None)
def get_origin_url(ctx: IContext):
    origin_url = None
    git_remote_stdout = get_git_output(ctx, ['remote'])
    if git_remote_stdout:
        lines = git_remote_stdout.splitlines()
        if 'origin' in lines:
            origin_url = get_git_output(ctx, ['remote', 'get-url', 'origin'])
    return origin_url

class GitMetadataProvider(BaseMetadataProvider):
    'the metadata provider base on git system.'

    def get_homepage_url(self, ctx: IContext) -> Optional[str]:
        origin_url = get_origin_url(ctx)
        if origin_url:
            from ..utils import parse_homepage_from_git_url
            return parse_homepage_from_git_url(origin_url)
