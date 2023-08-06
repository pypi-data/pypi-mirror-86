import json
import os
from typing import Optional

from .resolver import Resolver


class Mockee:
    CACHE = {}

    def __init__(self, def_file: str, encoding='utf8'):
        self.def_file = os.path.abspath(def_file)
        self.encoding = encoding

    def load(self):
        """
        从文件加载定义
        :return:
        """
        with open(self.def_file, encoding=self.encoding, mode='r') as fp:
            self.CACHE[self.def_file] = json.load(fp)

    @property
    def mock_data(self) -> dict:
        if self.def_file not in self.CACHE:
            self.load()

        return self.CACHE[self.def_file]

    def make(self, data_id: str, options: dict) -> [Optional[dict], Optional[list]]:
        if data_id not in self.mock_data:
            return None

        resolver = Resolver(self.mock_data[data_id], os.path.dirname(self.def_file), self.encoding, options)
        return resolver.resolve()
