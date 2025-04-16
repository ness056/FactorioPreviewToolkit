"""Entry point for the Factorio Preview Toolkit.

This tool detects map exchange strings (e.g. from clipboard), generates
preview images for all configured planets using the Factorio CLI, and optionally
uploads them to a remote service like Dropbox.
"""

# enable_tee_logging()

from src.FactorioPreviewToolkit.controller.controller import PreviewController
from src.FactorioPreviewToolkit.shared.structured_logger import log

if __name__ == "__main__":
    log.info("🚀 Factorio preview toolkit started.")
    try:
        controller = PreviewController()
        try:
            controller.start()
        except KeyboardInterrupt:
            controller.stop()
            log.info("👋 Interrupted by user. Shutting down...")
    finally:
        log.info("👋 Factorio preview Toolkit exited.")
