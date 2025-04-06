import sys
from pathlib import Path


def get_local_log_path(filename: str) -> Path:
    return Path(sys.argv[0]).resolve().parent / filename


LOCAL_LOG_PATH = get_local_log_path("preview_generator.log")
