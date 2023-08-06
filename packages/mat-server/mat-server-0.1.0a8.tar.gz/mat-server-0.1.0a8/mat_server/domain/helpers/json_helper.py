import abc
from typing import Any

from mat_server.domain import base_types


class JSONHelperBase(base_types.Helper):

    @abc.abstractmethod
    def serialize(self, data: Any) -> str:
        pass
