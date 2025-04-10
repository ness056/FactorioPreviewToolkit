# src/controller/system_monitor.py

import threading
import time
from queue import Queue
from typing import Optional

from src.factorio_path_provider.base import FactorioLocator
from src.map_string_provider.base import MapStringProvider
from src.shared.structured_logger import log


class SystemMonitor:
    def __init__(
        self,
        map_string_provider: MapStringProvider,
        factorio_locator: FactorioLocator,
    ):
        self._map_string_provider = map_string_provider
        self._factorio_locator = factorio_locator
        self._callback_queue = Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._latest_map_string: Optional[str] = None
        self._latest_factorio_path = None

    def start(self):
        log.info("🔍 Starting SystemMonitor thread...")
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()
        log.info("🛑 SystemMonitor stopped.")

    def _run_loop(self):
        while not self._stop_event.is_set():
            # Check for map string updates
            map_string = self._map_string_provider.poll_for_map_string()
            if map_string and map_string != self._latest_map_string:
                self._latest_map_string = map_string
                self._callback_queue.put(("map_string", map_string))

            # Always update latest factorio path
            factorio_path = self._factorio_locator.get_path()
            if factorio_path != self._latest_factorio_path:
                self._latest_factorio_path = factorio_path
                self._callback_queue.put(("factorio_path", factorio_path))

            time.sleep(0.5)  # Tune interval as needed

    def get_update(self) -> Optional[tuple[str, str]]:
        try:
            return self._callback_queue.get_nowait()
        except Exception:
            return None

    def get_latest_map_string(self) -> Optional[str]:
        return self._latest_map_string

    def get_latest_factorio_path(self):
        return self._latest_factorio_path
