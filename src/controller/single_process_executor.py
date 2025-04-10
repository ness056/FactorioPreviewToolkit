import subprocess
import sys
from enum import Enum, auto
from threading import Lock
from typing import Optional

from src.shared.structured_logger import log


class SubprocessStatus(Enum):
    NOT_RUN = auto()
    SUCCESS = auto()
    FAILED = auto()
    KILLED = auto()
    RUNNING = auto()


class SingleProcessExecutor:
    def __init__(self, process_name: str, args: list[str]):
        """
        Initializes the SingleProcessExecutor with a given process name and the arguments
        that should be passed to the subprocess.
        """
        self._process_name = process_name
        self._args = args
        self._active_process: Optional[subprocess.Popen] = None
        self._status = SubprocessStatus.NOT_RUN
        self._lock = Lock()  # Lock to ensure only one subprocess runs at a time

    def run_subprocess(self) -> SubprocessStatus:
        """
        Executes a subprocess with the provided arguments. If a process is already running,
        it will not start another.
        """
        with self._lock:
            if self._status != SubprocessStatus.NOT_RUN:
                return self._status

            # Start the subprocess
            log.info(
                f"🚀 Launching {self._process_name} subprocess with args: {self._args}..."
            )
            self._active_process = subprocess.Popen(
                [sys.executable, "-u"] + self._args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self._status = SubprocessStatus.RUNNING

        try:
            for line in self._active_process.stdout:
                print(line, end="")  # Forward to console/log
        except Exception:
            self._status = SubprocessStatus.FAILED
            log.error(f"❌ Failed to read {self._process_name} output.")
            raise

        # Wait for subprocess to finish and check its exit code
        exit_code = self._active_process.wait()

        with self._lock:
            # Check if the process was killed externally before completing
            if self._status == SubprocessStatus.KILLED:
                log.info(f"⚠️ {self._process_name} was killed externally.")
            elif exit_code == 0:
                self._status = SubprocessStatus.SUCCESS
            else:
                self._status = SubprocessStatus.FAILED
            return self._status

    def stop(self) -> bool:
        """
        Stops the active subprocess if it is running. Returns whether the stop was successful.
        """
        with self._lock:
            if self._active_process is None or self._status not in [
                SubprocessStatus.RUNNING,
                SubprocessStatus.NOT_RUN,
            ]:
                log.warning(f"⚠️ No active process to stop for {self._process_name}.")
                return False

            # Kill the active subprocess if it's running
            log.info(f"🛑 Stopping {self._process_name} subprocess...")
            self._active_process.kill()
            self._status = SubprocessStatus.KILLED
            log.info(f"✅ {self._process_name} subprocess killed.")
            return True

    def get_status(self) -> SubprocessStatus:
        """
        Returns the current status of the subprocess.
        """
        return self._status
