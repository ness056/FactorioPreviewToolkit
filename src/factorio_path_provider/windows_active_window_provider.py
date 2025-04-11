from pathlib import Path
from typing import Callable, Optional

import psutil
import win32gui
import win32process

from src.factorio_path_provider.active_window_provider import ActiveWindowProvider
from src.shared.structured_logger import log


class WindowsActiveWindowProvider(ActiveWindowProvider):
    """
    Windows-specific implementation of ActiveWindowProvider.
    """

    def __init__(self, on_new_factorio_path: Callable[[Path], None]):
        super().__init__(on_new_factorio_path)

    def get_factorio_executable_path(self) -> Optional[Path]:
        try:
            hwnd = win32gui.GetForegroundWindow()
            if hwnd == 0:
                return None
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            executable_path = process.exe()
            if "factorio.exe" in executable_path.lower():
                return Path(executable_path)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            log.error(f"Error getting Factorio executable path: {e}")
            return None
        return None
