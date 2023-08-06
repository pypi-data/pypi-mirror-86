# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import *

from ..bases import (
    BaseMetadataProvider, IContext,
    LongDescription
)

class FileSystemMetadataProvider(BaseMetadataProvider):
    'the metadata provider base on file system.'

    def get_long_description(self, ctx: IContext) -> Optional[LongDescription]:
        rst = ctx.get_text_content('README.rst')
        if rst is not None:
            return LongDescription(
                long_description=rst,
                long_description_content_type=None
            )

        md = ctx.get_text_content('README.md')
        if md is not None:
            return LongDescription(
                long_description=md,
                long_description_content_type='text/markdown'
            )

