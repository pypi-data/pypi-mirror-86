import random
import re
import uuid
from typing import List

from mat_server.domain import base_types


class TemplateService(base_types.Service):

    def substitute(self, template: str, replace_funcs: List[str]) -> str:
        for replace_func in replace_funcs:
            if replace_func == 'uuid_v4':
                template = self._transform_for_uuid_v4_replace_func(template)
            elif replace_func == 'random_int':
                template = self._transform_for_random_int_replace_func(template)
        return template

    @staticmethod
    def _transform_for_uuid_v4_replace_func(data: str) -> str:
        for _ in range(data.count('{uuid_v4()}')):
            data = data.replace('{uuid_v4()}', str(uuid.uuid4()), 1)
        return data

    @staticmethod
    def _transform_for_random_int_replace_func(data: str) -> str:
        for func, start, end in re.findall(r'(\{random_int\((\d+),\s*(\d+)\)\})', data):
            start, end = int(start), int(end)
            random_int = random.randint(start, end)
            data = data.replace(func, str(random_int), 1)
        return data
