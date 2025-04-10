from pathlib import Path
from typing import Callable

from src.factorio_path_provider.base import FactorioPathProvider
from src.shared.config import Config
from src.shared.structured_logger import log


class FixedPathProvider(FactorioPathProvider):
    def __init__(self, on_new_factorio_path: Callable[[Path], None]):
        super().__init__(on_new_factorio_path)

    def start(self) -> None:
        config = Config.get()
        fixed_path = config.factorio_executable
        log.info(f"📌 Using fixed Factorio path: {fixed_path}")
        self._on_new_factorio_path(fixed_path)

    def stop(self) -> None:
        # No background thread to stop
        log.info("✅ FixedPathProvider does not require cleanup.")
