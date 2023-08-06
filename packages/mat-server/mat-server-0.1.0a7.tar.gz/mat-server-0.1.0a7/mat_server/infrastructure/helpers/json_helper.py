from typing import Any

from mat_server.domain import helpers


class JSONHelper(helpers.JSONHelperBase):

    def __init__(self,
                 json_module):
        self._json_module = json_module

    def serialize(self, data: Any) -> str:
        return self._json_module.dumps(data)
