import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from src.FactorioPreviewToolkit.shared.shared_constants import constants
from src.FactorioPreviewToolkit.shared.structured_logger import log


def wait_for_factorio_lock_to_release(timeout_in_sec: int = 30) -> bool:
    """
    Waits for the Factorio lock file to be released, up to a timeout.
    """
    start_time = time.time()
    lock_file = constants.FACTORIO_LOCK_FILEPATH

    while lock_file.exists():
        log.info(f"📋 Waiting for '{lock_file}' release.")
        if time.time() - start_time > timeout_in_sec:
            log.error(f"❌ Timeout: Lock file still exists after {timeout_in_sec}s.")
            raise TimeoutError(f"Lock file '{lock_file}' still exists.")
        time.sleep(1)

    return True


def _build_factorio_command(executable_path: Path, args: list[str], config_path: Path) -> list[str]:
    """
    Builds the full Factorio CLI command with resolved paths and config file.
    """
    resolved_args = [str(Path(arg).resolve()) if not arg.startswith("--") else arg for arg in args]
    return [str(executable_path), "--config", str(config_path)] + resolved_args


def _build_subprocess_kwargs() -> dict[str, Any]:
    """
    Builds default subprocess.run kwargs with logging and priority settings.
    """
    return {
        "check": True,
        "capture_output": True,
        "text": True,
        **_get_priority_settings(),
    }


def _get_priority_settings() -> dict[str, Any]:
    """
    Returns platform-specific CPU priority settings for subprocess.run.
    """
    if sys.platform == "win32":
        return {"creationflags": subprocess.IDLE_PRIORITY_CLASS}
    elif sys.platform in ("linux", "darwin"):
        return {"preexec_fn": lambda: os.nice(19)}
    return {}


def run_factorio_command(factorio_executable_path: Path, args: list[str]) -> None:
    """
    Runs Factorio with the given args and config, with low-priority CPU settings.
    """
    config_path = constants.FACTORIO_CONFIG_PATH
    log.info(f"Using config file: {config_path}")

    try:
        wait_for_factorio_lock_to_release()
        cmd = _build_factorio_command(factorio_executable_path, args, config_path)
        kwargs = _build_subprocess_kwargs()
        subprocess.run(cmd, **kwargs)

    except FileNotFoundError:
        log.error("❌ Factorio executable not found.")
        raise
    except subprocess.CalledProcessError as e:
        log.error("❌ Factorio execution failed.")
        log.error(f"stdout:\n{e.stdout}")
        log.error(f"stderr:\n{e.stderr}")
        raise
