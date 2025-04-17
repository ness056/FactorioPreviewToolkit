"""Entry point for the Factorio Preview Toolkit.

This tool detects map exchange strings (e.g. from clipboard), generates
preview images for all configured planets using the Factorio CLI, and optionally
uploads them to a remote service like Dropbox.
"""

from src.FactorioPreviewToolkit.shared.error_popup import show_error_popup
from src.FactorioPreviewToolkit.shared.shared_constants import constants
from src.FactorioPreviewToolkit.shared.tee_logger import enable_tee_logging

enable_tee_logging(constants.LOGS_DIR, keep_last_n=20)

from src.FactorioPreviewToolkit.controller.controller import PreviewController
from src.FactorioPreviewToolkit.shared.structured_logger import log

if __name__ == "__main__":
    log.info("🚀 Factorio preview toolkit started.")
    controller = None
    try:
        controller = PreviewController()
        controller.start()
    except KeyboardInterrupt:
        log.info("👋 Interrupted by user. Shutting down...")
    except Exception as e:
        log.exception("❌ Unhandled exception occurred.")
        show_error_popup("Factorio Toolkit Error", str(e))  # ← friendly UI for users
        raise
    finally:
        if controller is not None:
            controller.stop()
        log.info("👋 Factorio preview Toolkit exited.")
