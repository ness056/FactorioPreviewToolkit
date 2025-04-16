import sys
from io import TextIOBase, BufferedWriter
from pathlib import Path
from typing import TextIO, cast

from src.FactorioPreviewToolkit.shared.shared_constants import constants


class TeeOutput(TextIOBase):
    """
    Custom output stream that duplicates stdout/stderr to a log file.
    """

    def __init__(self, path: Path):
        self.terminal = sys.__stdout__
        self.log: TextIO | None = open(path, "w", encoding="utf-8")
        self.buffer: BufferedWriter = self.terminal.buffer

    def write(self, message: str) -> int:
        """
        Writes a message to both the terminal and the log file.
        """
        if self.terminal:
            self.terminal.write(message)
        if self.log:
            self.log.write(message)
        return len(message)

    def flush(self) -> None:
        """
        Flushes both the terminal and the log file.
        """
        if self.terminal:
            self.terminal.flush()
        if self.log:
            self.log.flush()


def enable_tee_logging() -> None:
    """
    Redirects stdout and stderr to both the console and a rotated log file.
    Rotates LOG_PATH → PREVIOUS_LOG_PATH if it exists.
    """
    current_log = constants.LOG_PATH
    previous_log = constants.PREVIOUS_LOG_PATH
    log_dir = current_log.parent
    log_dir.mkdir(parents=True, exist_ok=True)

    # Rotate current → previous
    if current_log.exists():
        if previous_log.exists():
            previous_log.unlink()
        current_log.rename(previous_log)

    # Apply redirection (cast to TextIO to satisfy mypy)
    sys.stdout = sys.stderr = cast(TextIO, TeeOutput(current_log))
