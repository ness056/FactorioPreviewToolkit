# src/main.py or __main__.py

from src.controller.controller import PreviewController
from src.shared.structured_logger import log

if __name__ == "__main__":
    log.info("🚀 Factorio preview toolkit started.")
    try:
        controller = PreviewController()
        controller.run()
    finally:
        log.info("👋 Factorio preview Toolkit exited.")
