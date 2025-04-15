import re
import sys
from pathlib import Path


def is_valid_map_string(s: str) -> bool:
    return bool(re.match(r"^>>>eN[a-zA-Z0-9+/=]+<<<$", s.strip()))


def get_project_root() -> Path:
    """
    Detects the root directory of the project, whether running from source or from a frozen executable.
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parents[3]  # adjust if needed based on actual file depth


def resolve_relative_to_project_root(path: str | Path) -> Path:
    """
    Resolves the given path relative to the project root, unless it's already absolute.
    """
    path = Path(path)
    if path.is_absolute():
        return path
    return (get_project_root() / path).resolve()
