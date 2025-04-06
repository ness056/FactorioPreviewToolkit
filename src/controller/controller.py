# src/controller/controller.py

import subprocess
import sys
from threading import Lock, Thread
from typing import Optional

from src.map_string_provider.factory import get_map_string_provider
from src.shared.config_loader import get_config
from src.shared.sound import play_sound
from src.shared.structured_logger import log


class PreviewController:
    def __init__(self):
        self._config = get_config()
        self._provider = get_map_string_provider(self._config.map_exchange_input_method)
        self._preview_process: Optional[subprocess.Popen] = None
        self._upload_process: Optional[subprocess.Popen] = None
        self._worker_thread: Optional[Thread] = None
        self._worker_counter = 1
        self._lock = Lock()

    def _stop_preview_generator(self):
        with self._lock:
            if self._preview_process and self._preview_process.poll() is None:
                log.info("🛑 Killing preview generator...")
                self._preview_process.kill()
                log.info("✅ Preview generator killed.")
            self._preview_process = None

    def _stop_uploader(self):
        with self._lock:
            if self._upload_process and self._upload_process.poll() is None:
                log.info("🛑 Killing uploader...")
                self._upload_process.kill()
                log.info("✅ Uploader killed.")
            self._upload_process = None

    def _start_preview_generator(self, map_string: str) -> Optional[bool]:
        log.info("🚀 Launching preview generator...")
        process = subprocess.Popen(
            [sys.executable, "-u", "-m", "src.preview_generator", map_string],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self._preview_process = process

        try:
            for line in process.stdout:
                print(line, end="")  # Forward to console/log
        except Exception as e:
            log.error(f"❌ Failed to read generator output: {e}")

        exit_code = process.wait()
        if process.poll() is None:
            return None  # Killed externally
        return exit_code == 0

    def _start_uploader(self) -> Optional[bool]:
        log.info("🌐 Starting uploader...")
        process = subprocess.Popen(
            [sys.executable, "-u", "-m", "src.uploader"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self._upload_process = process

        try:
            for line in process.stdout:
                print(line, end="")  # Forward to console/log
        except Exception as e:
            log.error(f"❌ Failed to read uploader output: {e}")

        exit_code = process.wait()
        if process.poll() is None:
            return None  # Killed externally
        return exit_code == 0

    def _on_start(self):
        play_sound(self._config.sound_start_file, self._config.sound_volume_start_file)

    def _on_success(self):
        play_sound(
            self._config.sound_success_file, self._config.sound_volume_success_file
        )

    def _on_failure(self):
        play_sound(
            self._config.sound_failure_file, self._config.sound_volume_failure_file
        )

    def _start_pipeline(self, map_string: str):
        self._on_start()

        success = self._start_preview_generator(map_string)
        if success is None:
            return  # Aborted, no sound
        if not success:
            self._on_failure()
            return

        success = self._start_uploader()
        if success is None:
            return  # Aborted, no sound
        if not success:
            self._on_failure()
            return

        self._on_success()

    def run(self):
        log.info("🧠 Controller initialized. Listening for map exchange strings...")
        try:
            while True:
                map_string = self._provider.wait_for_map_string()
                log.info("📥 New map exchange string received.")

                # Cancel any running job
                if self._worker_thread and self._worker_thread.is_alive():
                    log.info("🧹 Interrupting previous pipeline...")
                    self._stop_preview_generator()
                    self._stop_uploader()

                # Start new pipeline thread
                thread_name = f"Worker-{self._worker_counter}"
                self._worker_counter += 1

                self._worker_thread = Thread(
                    target=self._start_pipeline,
                    args=(map_string,),
                    name=thread_name,
                )
                self._worker_thread.start()

        except KeyboardInterrupt:
            log.info("🛑 Controller interrupted by user.")
        finally:
            self._stop_preview_generator()
            self._stop_uploader()
            log.info("👋 Controller shutdown complete.")
