import subprocess
import sys
from pathlib import Path
from typing import List

from src.shared.shared_constants import constants
from src.shared.structured_logger import log


def get_factorio_executable(factorio_base_path: Path) -> Path:
    """Returns the full path to the Factorio executable, OS-specific."""
    if sys.platform.startswith("win"):
        return factorio_base_path / "bin" / "x64" / "factorio.exe"
    elif sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        return factorio_base_path  # User must provide correct path
    else:
        raise RuntimeError(f"Unsupported platform: {sys.platform}")


def run_factorio_command(factorio_executable_path: Path, args: List[str]) -> None:
    """Executes Factorio with the given executable path, config file, and CLI arguments."""

    # Hardcoding the config path for now
    config_path = constants.FACTORIO_CONFIG_PATH

    # Log the configuration file being used
    log.info(f"Using config file: {config_path}")

    # Resolve all args that are not flags (e.g., not starting with --)
    resolved_args = [
        str(Path(arg).resolve()) if not arg.startswith("--") else arg for arg in args
    ]

    # Include the --config flag and the config file as the second parameter to the command
    cmd = [
        str(factorio_executable_path),
        "--config",
        str(config_path),
    ] + resolved_args  # Factorio path, --config, config file, then other args

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except FileNotFoundError:
        log.error("❌ Factorio executable not found.")
        raise
    except subprocess.CalledProcessError as e:
        log.error("❌ Factorio execution failed.")
        log.error(f"stdout:\n{e.stdout}")
        log.error(f"stderr:\n{e.stderr}")
        raise
