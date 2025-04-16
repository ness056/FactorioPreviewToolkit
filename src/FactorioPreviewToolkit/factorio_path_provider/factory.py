import collections
import platform
from pathlib import Path

from src.FactorioPreviewToolkit.factorio_path_provider.base import FactorioPathProvider
from src.FactorioPreviewToolkit.factorio_path_provider.fixed_path_provider import FixedPathProvider
from src.FactorioPreviewToolkit.factorio_path_provider.windows_active_window_provider import (
    WindowsActiveWindowProvider,
)
from src.FactorioPreviewToolkit.shared.config import Config
from src.FactorioPreviewToolkit.shared.structured_logger import log


def get_factorio_path_provider(
    on_new_factorio_path: collections.abc.Callable[[Path], None],
) -> FactorioPathProvider:
    """
    Factory function that returns a FactorioPathProvider implementation
    based on the configured locator method and operating system.
    """
    config = Config.get()
    method = config.factorio_locator_method

    if method == "fixed_path":
        log.info("🏗️ Using FixedPathProvider")
        return FixedPathProvider(on_new_factorio_path)

    elif method == "active_window":
        log.info("🏗️ Using ActiveWindowProvider")

        system = platform.system()
        if system == "Windows":
            return WindowsActiveWindowProvider(on_new_factorio_path)
        # elif system == "Darwin":  # macOS  # TODO: AntiElitz: Implement active window provider for Mac
        #     return MacActiveWindowProvider(on_new_factorio_path)
        # elif system == "Linux":  # TODO: AntiElitz: Implement active window provider for Linux
        #     return LinuxActiveWindowProvider(on_new_factorio_path)
        else:
            raise ValueError(f"❌ Unsupported platform: {system}")

    else:
        raise ValueError(f"❌ Unknown factorio_locator_method: {method}")
