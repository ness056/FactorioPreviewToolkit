import collections
import threading
import time
from abc import abstractmethod
from pathlib import Path

from src.factorio_path_provider.base import FactorioPathProvider
from src.shared.config import Config
from src.shared.structured_logger import log


class ActiveWindowProvider(FactorioPathProvider):
    def __init__(self, on_new_factorio_path: collections.abc.Callable[[Path], None]):
        """
        Abstract base class that continuously monitors the active window to determine if it belongs to a Factorio process.
        When a new Factorio window is detected, the executable path of the running Factorio process is passed to the provided callback.
        """
        super().__init__(on_new_factorio_path)
        self._current_path: Path | None = None
        self._poll_interval = Config.get().active_window_poll_interval_in_seconds
        self._stop_flag = threading.Event()
        self._thread = threading.Thread(
            target=self._run, name="ActiveWindowWatcher", daemon=False
        )

    def start(self) -> None:
        """Start monitoring the active window."""
        log.info(
            f"🚀 Starting Active Window Provider monitoring with a poll interval of {self._poll_interval} seconds..."
        )
        self._stop_flag.clear()
        self._thread.start()

    def stop(self) -> None:
        """Stop the active window monitoring."""
        log.info("🛑 Stopping Active Window Provider monitoring...")
        self._stop_flag.set()
        self._thread.join()
        log.info("✅ Active Window Provider monitoring stopped.")

    def _run(self) -> None:
        """Continuously check the active window and update the Factorio path."""
        while not self._stop_flag.is_set():
            factorio_path = self.get_factorio_executable_path()

            if factorio_path and self._current_path != factorio_path:
                log.info(f"🪟 Detected new Factorio path: {factorio_path}")
                self._current_path = factorio_path
                self._on_new_factorio_path(factorio_path)

            time.sleep(self._poll_interval)

    @abstractmethod
    def get_factorio_executable_path(self) -> Path | None:
        """
        This method must be implemented in each platform-specific subclass to fetch the Factorio executable path
        from the currently active window.
        """
        pass
