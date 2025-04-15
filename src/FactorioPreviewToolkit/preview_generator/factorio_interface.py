import subprocess
import time
from pathlib import Path

from src.FactorioPreviewToolkit.shared.shared_constants import constants
from src.FactorioPreviewToolkit.shared.structured_logger import log


def wait_for_factorio_lock_to_release(timeout_in_sec: int = 30) -> bool:
    start_time = time.time()
    lock_file = constants.FACTORIO_LOCK_PATH
    while lock_file.exists():
        log.info(f"📋 Waiting for '{lock_file}' release.")
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout_in_sec:
            log.error(
                f"❌ Timeout: Lock file '{lock_file}' still exists after {timeout_in_sec} seconds."
            )
            raise TimeoutError(
                f"Lock file '{lock_file}' still exists after {timeout_in_sec} seconds."
            )
        time.sleep(1)
    return True


def run_factorio_command(factorio_executable_path: Path, args: list[str]) -> None:
    """Executes Factorio with the given executable path, config file, and CLI arguments."""

    # Hardcoding the config path for now
    config_path = constants.FACTORIO_CONFIG_PATH

    # Log the configuration file being used
    log.info(f"Using config file: {config_path}")

    # Resolve all args that are not flags (e.g., not starting with --)
    resolved_args = [str(Path(arg).resolve()) if not arg.startswith("--") else arg for arg in args]

    # Include the --config flag and the config file as the second parameter to the command
    cmd = [
        str(factorio_executable_path),
        "--config",
        str(config_path),
    ] + resolved_args  # Factorio path, --config, config file, then other args

    try:
        wait_for_factorio_lock_to_release()
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except FileNotFoundError:
        log.error("❌ Factorio executable not found.")
        raise
    except subprocess.CalledProcessError as e:
        log.error("❌ Factorio execution failed.")
        log.error(f"stdout:\n{e.stdout}")
        log.error(f"stderr:\n{e.stderr}")
        raise
