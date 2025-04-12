import sys
from pathlib import Path
from typing import TextIO


class TeeOutput:
    def __init__(self, path: Path):
        self.terminal = sys.__stdout__
        self.log: TextIO | None = open(
            path, "w", encoding="utf-8"
        )  # Type annotation added for the log

    def write(self, message: str) -> None:
        """Writes message to both terminal and log."""
        if self.log and self.terminal:
            self.terminal.write(message)
            self.log.write(message)

    def flush(self) -> None:
        """Flushes both terminal and log."""
        if self.log and self.terminal:
            self.terminal.flush()
            self.log.flush()


def enable_tee_logging(log_path: Path) -> None:
    """
    Redirect stdout and stderr to both the console and a rotated log file.
    Rotates <log_path> → previous.log if it exists.
    """
    log_dir = log_path.parent
    log_dir.mkdir(parents=True, exist_ok=True)

    current_log = log_path
    previous_log = log_dir / "previous.log"

    # Rotate current → previous
    if current_log.exists():
        if previous_log.exists():
            previous_log.unlink()
        current_log.rename(previous_log)

    # Apply redirection
    sys.stdout = sys.stderr = TeeOutput(current_log)
