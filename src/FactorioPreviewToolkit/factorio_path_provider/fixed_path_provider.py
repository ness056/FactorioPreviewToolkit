import collections
from pathlib import Path

from src.FactorioPreviewToolkit.factorio_path_provider.base import FactorioPathProvider
from src.FactorioPreviewToolkit.shared.config import Config
from src.FactorioPreviewToolkit.shared.structured_logger import log


class FixedPathProvider(FactorioPathProvider):
    def __init__(self, on_new_factorio_path: collections.abc.Callable[[Path], None]):
        super().__init__(on_new_factorio_path)

    def start(self) -> None:
        config = Config.get()
        fixed_path = config.fixed_path_factorio_executable
        assert (
            fixed_path is not None
        ), "Internal error: fixed_path_factorio_executable should have been validated by config schema"
        log.info(f"📌 Using fixed Factorio path: {fixed_path}")
        self._on_new_factorio_path(fixed_path)

    def stop(self) -> None:
        # No background thread to stop
        log.info("✅ FixedPathProvider does not require cleanup.")
