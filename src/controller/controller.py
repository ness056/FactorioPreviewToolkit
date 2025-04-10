import queue
from pathlib import Path
from queue import Queue
from typing import Optional

from src.controller.map_processing_pipeline import MapProcessingPipeline
from src.factorio_path_provider.factory import get_factorio_path_provider
from src.map_string_provider.factory import get_map_string_provider
from src.shared.structured_logger import log


class PreviewController:
    """
    A controller for managing map processing pipeline for Factorio map previews.

    This controller listens for map strings and Factorio paths asynchronously and processes them
    by running the map preview generation and upload tasks. Only one task is executed at a time,
    and if a new task starts, the old task is aborted.
    """

    def __init__(self):
        """
        Initializes the PreviewController with required resources.
        """
        self._running = False
        self._factorio_path_provider = None
        self._map_string_provider = None

        self._latest_factorio_path: Optional[Path] = None
        self._latest_map_string: Optional[str] = None
        self._map_string_analysed = False

        self._event_queue = Queue()
        self._map_processing_pipeline = MapProcessingPipeline()

    def _process_events(self):
        """
        Processes events from the event queue. This method listens for new map strings and Factorio paths,
        and triggers the map processing pipeline when both are available.
        """
        while self._running:
            try:
                event_type, data = self._event_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            if event_type == "map_string":
                self._latest_map_string = data
                self._map_string_analysed = False

            elif event_type == "factorio_path":
                self._latest_factorio_path = data

            if (
                self._latest_map_string
                and self._latest_factorio_path
                and not self._map_string_analysed
            ):
                self._start_map_processing()

    def _start_map_processing(self):
        """
        Starts the map processing pipeline with the latest map string and Factorio path.
        """
        self._map_string_analysed = True
        self._map_processing_pipeline.run_async(
            self._latest_factorio_path, self._latest_map_string
        )

    def stop(self):
        """
        Stops the map processing pipeline and cleans up resources.
        """
        if self._map_string_provider:
            self._map_string_provider.stop()
        if self._factorio_path_provider:
            self._factorio_path_provider.stop()
        log.info("👋 Controller stopped successfully.")
        self._running = False

    def start(self):
        """
        Starts the PreviewController to process map strings and Factorio paths asynchronously.
        """

        def on_new_map_string(map_string: str):
            log.info(f"📥 Received new map string: {map_string}")
            self._event_queue.put(("map_string", map_string))

        def on_new_factorio_path(factorio_path: Path):
            log.info(f"📍 Detected new Factorio path: {factorio_path}")
            self._event_queue.put(("factorio_path", factorio_path))

        self._map_string_provider = get_map_string_provider(on_new_map_string)
        self._factorio_path_provider = get_factorio_path_provider(on_new_factorio_path)

        self._map_string_provider.start()
        self._factorio_path_provider.start()

        self._running = True
        self._process_events()
