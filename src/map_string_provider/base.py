import re
from abc import ABC, abstractmethod


class BaseMapStringProvider(ABC):
    @abstractmethod
    def wait_for_map_string(self) -> str:
        pass

    @staticmethod
    def _is_valid_map_string(s: str) -> bool:
        return bool(re.match(r"^>>>eN[a-zA-Z0-9+/=]+<<<$", s.strip()))
