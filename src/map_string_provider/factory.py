# src/core/mapstring_providers/factory.py

from .base import BaseMapStringProvider
from .clipboard_provider import ClipboardMapStringProvider

# from .file_map_string_provider import FileMapStringProvider


def get_map_string_provider(method: str) -> BaseMapStringProvider:
    match method:
        case "clipboard_auto":
            return ClipboardMapStringProvider()
        # case "file_watch":
        #     return FileMapStringProvider()
        case _:
            raise ValueError(f"Unsupported map exchange input method: '{method}'")
