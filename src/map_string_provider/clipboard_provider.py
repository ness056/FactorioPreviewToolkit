# src/map_string_provider/clipboard_provider.py

import time

import pyperclip

from src.map_string_provider.base import BaseMapStringProvider
from src.shared.structured_logger import log


class ClipboardMapStringProvider(BaseMapStringProvider):
    def __init__(self, poll_interval: float = 0.5):
        self._last_map_string = ""
        self._poll_interval = poll_interval

    def wait_for_map_string(self) -> str:
        log.info("📋 Monitoring clipboard for new map exchange strings...")
        while True:
            try:
                clipboard_text = pyperclip.paste().strip()
                if (
                    clipboard_text != self._last_map_string
                    and self._is_valid_map_string(clipboard_text)
                ):
                    log.info("🎯 New map exchange string detected in clipboard.")
                    self._last_map_string = clipboard_text
                    return clipboard_text
            except Exception as e:
                log.warning(f"⚠️ Failed to read clipboard: {e}")
            time.sleep(self._poll_interval)
