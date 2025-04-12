from pathlib import Path
from threading import Lock, Thread

from src.controller.single_process_executor import (
    SubprocessStatus,
    SingleProcessExecutor,
)
from src.shared.sound import play_failure_sound, play_success_sound, play_start_sound
from src.shared.structured_logger import log


class MapProcessingPipeline:
    """
    This class represents a pipeline for processing a Factorio map. It executes two subprocesses
    sequentially: a preview generation and an upload step. The pipeline runs asynchronously,
    with only one worker executing at a time. If a new job is triggered while the current pipeline
    is running, the previous job is interrupted as the result is no longer needed.
    """

    def __init__(self):
        self.generator_executor: SingleProcessExecutor | None = None
        self.uploader_executor: SingleProcessExecutor | None = None
        self._lock = Lock()
        self._worker_thread: Thread | None = None
        self._worker_ID = 0

    def run_async(self, factorio_path: Path, map_string: str) -> None:
        self._stop()
        with self._lock:
            self.generator_executor = SingleProcessExecutor(
                "Preview Generator",
                ["-m", "src.preview_generator", str(factorio_path), map_string],
            )
            self.uploader_executor = SingleProcessExecutor(
                "Uploader", ["-m", "src.uploader", str(factorio_path)]
            )

            thread_name = f"Worker-{self._worker_ID}"
            self._worker_ID += 1
            self._worker_thread = Thread(
                target=self._execute_pipeline,
                args=(),
                name=thread_name,
                daemon=True,
            )
            self._worker_thread.start()

    def _execute_pipeline(self):
        with self._lock:

            play_start_sound()

            generator_status = self.generator_executor.run_subprocess()
            if generator_status == SubprocessStatus.KILLED:
                return
            if generator_status != SubprocessStatus.SUCCESS:
                play_failure_sound()
                return

            upload_status = self.uploader_executor.run_subprocess()
            if upload_status == SubprocessStatus.KILLED:
                return
            if upload_status != SubprocessStatus.SUCCESS:
                play_failure_sound()
                return

            play_success_sound()

    def _stop(self) -> None:

        if self.generator_executor and self.generator_executor.get_status() in [
            SubprocessStatus.RUNNING,
            SubprocessStatus.NOT_RUN,
        ]:
            self.generator_executor.stop()

        if self.uploader_executor and self.uploader_executor.get_status() in [
            SubprocessStatus.RUNNING,
            SubprocessStatus.NOT_RUN,
        ]:
            self.uploader_executor.stop()

        if self._worker_thread and self._worker_thread.is_alive():
            log.info("⚠️ Pipeline is already running. Aborting...")
            self._worker_thread.join(timeout=1)
            if self._worker_thread.is_alive():
                log.error(
                    "❌ Worker thread did not terminate in time. Raising exception."
                )
                raise TimeoutError(
                    "Worker thread did not terminate within the expected time."
                )
