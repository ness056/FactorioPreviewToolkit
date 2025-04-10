# src/factorio_path_provider/factory.py

from pathlib import Path
from typing import Callable

from src.factorio_path_provider.active_window_provider import ActiveWindowProvider
from src.factorio_path_provider.base import FactorioPathProvider
from src.factorio_path_provider.fixed_path_provider import FixedPathProvider
from src.shared.config import Config
from src.shared.structured_logger import log


def get_factorio_path_provider(
    on_new_factorio_path: Callable[[Path], None],
) -> FactorioPathProvider:
    config = Config.get()
    method = config.factorio_locator_method

    if method == "fixed_path":
        log.info("🏗️ Using FixedPathProvider")
        return FixedPathProvider(on_new_factorio_path)
    elif method == "active_window":
        log.info("🏗️ Using ActiveWindowProvider")
        return ActiveWindowProvider(on_new_factorio_path)
    else:
        raise ValueError(f"❌ Unknown factorio_locator_method: {method}")
