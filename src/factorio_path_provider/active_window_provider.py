# src/factorio_path_provider/active_window_provider.py

import threading
import time
from pathlib import Path
from typing import Callable, Optional

from src.factorio_path_provider.base import FactorioPathProvider
from src.shared.structured_logger import log


class ActiveWindowProvider(FactorioPathProvider):
    def __init__(self, on_new_factorio_path: Callable[[Path], None]):
        super().__init__(on_new_factorio_path)
        self._current_path: Optional[Path] = None
        self._stop_flag = threading.Event()
        self._thread = threading.Thread(
            target=self._run, name="ActiveWindowWatcher", daemon=False
        )

    def start(self):
        log.info("🚀 Starting Active Window Provider monitoring...")
        self._stop_flag.clear()
        self._thread.start()

    def stop(self):
        log.info("🛑 Stopping Active Window Provider monitoring...")
        self._stop_flag.set()
        self._thread.join()
        log.info("✅ Active Window Provider monitoring stopped.")

    def _run(self):
        while not self._stop_flag.is_set():
            # TODO: Replace with actual active window path detection logic
            fake_path = Path("C:/Program Files/Factorio/bin/x64/factorio.exe")

            if self._current_path != fake_path:
                log.info(f"🪟 Detected new Factorio path: {fake_path}")
                self._current_path = fake_path
                self._on_new_factorio_path(fake_path)

            time.sleep(1)
