from src.FactorioPreviewToolkit.shared.structured_logger import log, log_section
from src.FactorioPreviewToolkit.uploader.factory import get_uploader


def main() -> None:
    log_section("🚀 Uploader started.")
    uploader = get_uploader()
    uploader.upload_all()
    log.info("✅ Uploader finished successfully.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        log.exception("❌ Uploader failed with an exception.")
        raise
    finally:
        log.info("👋 Uploader exited.")
