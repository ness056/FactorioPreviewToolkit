from src.FactorioPreviewToolkit.controller.controller import PreviewController
from src.FactorioPreviewToolkit.shared.structured_logger import log
from src.FactorioPreviewToolkit.shared.tee_logger import enable_tee_logging

# Enable terminal + file logging before anything else
enable_tee_logging()

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
