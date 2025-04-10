from abc import ABC, abstractmethod
from typing import Callable


class MapStringProvider(ABC):
    """
    Abstract base class for map string providers.
    Implementations must handle their own detection logic and call the callback
    when a valid map exchange string is detected.
    """

    def __init__(self, on_new_map_string: Callable[[str], None]):
        self._on_new_map_string = on_new_map_string

    @abstractmethod
    def start(self):
        """Start the map string monitoring (threaded or otherwise)."""
        pass

    @abstractmethod
    def stop(self):
        """Stop the monitoring and clean up if needed."""
        pass
