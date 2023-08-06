# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import *
from abc import ABC, abstractmethod
from dataclasses import dataclass

import fsoopify

class IContext(ABC):
    'the base context class.'

    @property
    @abstractmethod
    def state(self) -> dict:
        '''
        get a dict for store or load states.
        '''
        raise NotImplementedError

    @property
    @abstractmethod
    def root_path(self) -> fsoopify.Path:
        '''
        get the root path of project.
        '''
        raise NotImplementedError

    @abstractmethod
    def get_fileinfo(self, relpath: str) -> fsoopify.FileInfo:
        '''
        get a `FileInfo` by the relative path which relative to the root of project.
        '''
        raise NotImplementedError

    @abstractmethod
    def get_text_content(self, relpath: str) -> Optional[str]:
        '''
        try read file content as text from the relative path.

        return `None` if not exists.
        '''
        raise NotImplementedError


@dataclass
class LongDescription:
    long_description: str
    long_description_content_type: Optional[str]=None


class BaseMetadataProvider:
    ' the base metadata provider. '

    def get_long_description(self, ctx: IContext) -> Optional[LongDescription]:
        pass

    def get_homepage_url(self, ctx: IContext) -> Optional[str]:
        pass
