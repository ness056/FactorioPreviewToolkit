# src/map_string_provider/clipboard_provider.py
import collections
import threading
import time

import pyperclip

from src.FactorioPreviewToolkit.map_string_provider.base import MapStringProvider
from src.FactorioPreviewToolkit.shared.structured_logger import log, log_section
from src.FactorioPreviewToolkit.shared.utils import is_valid_map_string


class ClipboardMapStringProvider(MapStringProvider):
    def __init__(
        self,
        on_new_map_string: collections.abc.Callable[[str], None],
        poll_interval: float = 0.5,
    ):
        super().__init__(on_new_map_string)
        self._poll_interval = poll_interval
        self._last_map_string = ""
        self._stop_flag = threading.Event()
        self._thread = threading.Thread(
            target=self._run,
            name="ClipboardMonitor",
            daemon=False,
        )

    def start(self) -> None:
        log.info("🚀 Starting Clipboard Monitor...")
        self._stop_flag.clear()
        self._thread.start()

    def stop(self) -> None:
        log.info("🛑 Stopping Clipboard Monitor...")
        self._stop_flag.set()
        self._thread.join()
        log.info("✅ Clipboard Monitor stopped.")

    def _run(self) -> None:
        with log_section("📋 Monitoring clipboard for new map exchange strings..."):
            while not self._stop_flag.is_set():
                try:
                    clipboard_text = pyperclip.paste().strip()
                    if clipboard_text != self._last_map_string and is_valid_map_string(
                        clipboard_text
                    ):
                        log.info("🎯 New map exchange string detected in clipboard.")
                        self._last_map_string = clipboard_text
                        self._on_new_map_string(clipboard_text)
                except Exception as e:
                    log.warning(f"⚠️ Failed to read clipboard: {e}")
                time.sleep(self._poll_interval)
