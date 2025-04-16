import logging
import sys
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from io import TextIOWrapper

# Thread-local storage for nesting level (per thread)
_nesting = threading.local()


def get_logging_indent() -> str:
    """
    Returns the current indentation string based on nesting level.
    """
    level = getattr(_nesting, "level", 0)
    if level == 0:
        return ""
    return "   " * level  # Indentation string


@contextmanager
def log_section(title: str) -> Iterator[None]:
    """
    Context manager for logging a section with increased indentation.
    Restores indentation level after the block ends.
    """
    if not hasattr(_nesting, "level"):
        _nesting.level = 0

    log.info(title)
    _nesting.level += 1
    try:
        yield
    finally:
        _nesting.level = max(0, _nesting.level - 1)


def set_logging_indent(level: int) -> None:
    """
    Sets the current thread's indentation level manually.
    """
    if not hasattr(_nesting, "level"):
        _nesting.level = 0
    _nesting.level = max(0, level)


class IndentedFormatter(logging.Formatter):
    """
    Custom log formatter that adds process/thread metadata and supports indentation.
    """

    def format(self, record: logging.LogRecord) -> str:
        pid_part = f"PID:{record.process:>5}"
        thread_part = f"{record.threadName}"
        tag = f"[{pid_part}, {thread_part}]"
        level = f"{record.levelname:<5}"

        prefix = get_logging_indent()
        super().format(record)
        message = record.getMessage()

        formatted_msg = f"{record.asctime} {tag:<32} {level}: {message}"
        if prefix and record.levelno >= logging.INFO:
            return formatted_msg.replace(message, f"{prefix}{message}")
        return formatted_msg


def setup_logger() -> logging.Logger:
    """
    Sets up the structured logger with custom formatting and UTF-8 stdout handling.
    """
    # Ensure UTF-8 encoding for stdout/stderr
    if sys.stdout.encoding is None or sys.stdout.encoding.lower() != "utf-8":
        sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if sys.stderr.encoding is None or sys.stderr.encoding.lower() != "utf-8":
        sys.stderr = TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

    formatter = IndentedFormatter(
        "%(asctime)s [PID:%(process)d, %(threadName)s] %(levelname)s: %(message)s"
    )

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger("structured_logger")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(stream_handler)
    logger.propagate = False

    return logger


log = setup_logger()
