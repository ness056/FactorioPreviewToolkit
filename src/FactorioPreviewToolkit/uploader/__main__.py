from src.FactorioPreviewToolkit.shared.structured_logger import log, log_section
from src.FactorioPreviewToolkit.uploader.factory import get_uploader


def main() -> None:
    """
    Entry point for running the uploader standalone. Selects the uploader and starts the upload.
    Handles errors and ensures clean logging exit.
    """
    try:
        with log_section("🚀 Uploader started."):
            uploader = get_uploader()
            uploader.upload_all()
            log.info("✅ Uploader finished successfully.")
    except Exception:
        log.exception("❌ Uploader failed with an exception.")
        raise
    finally:
        log.info("👋 Uploader exited.")


if __name__ == "__main__":
    main()
