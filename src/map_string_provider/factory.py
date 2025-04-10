# src/map_string_provider/factory.py

from typing import Callable

from src.map_string_provider.base import MapStringProvider
from src.map_string_provider.clipboard_provider import ClipboardMapStringProvider
from src.shared.config import Config


def get_map_string_provider(
    on_new_map_string: Callable[[str], None],
) -> MapStringProvider:
    config = Config.get()
    map_exchange_input_method = config.map_exchange_input_method
    if map_exchange_input_method == "clipboard_auto":
        # Detect and handle clipboard-based input automatically
        return ClipboardMapStringProvider(on_new_map_string)
    # elif map_exchange_input_method == "file_watch":
    #     # Watch a file for changes and read map string
    #     return FileWatchMapStringProvider(on_new_map_string)
    else:
        raise ValueError(
            f"Unsupported map_exchange_input_method: {map_exchange_input_method}"
        )
