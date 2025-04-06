from src.shared.structured_logger import log, log_section
from src.shared.tee_logger import enable_tee_logging
from src.uploader.constants import LOCAL_LOG_PATH
from src.uploader.factory import get_uploader

enable_tee_logging(LOCAL_LOG_PATH)


def main():
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
