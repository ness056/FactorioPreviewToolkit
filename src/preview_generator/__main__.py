import argparse

from src.preview_generator.constants import LOCAL_LOG_PATH
from src.preview_generator.generate_previews import (
    generate_previews_from_map_string,
)
from src.shared.structured_logger import log, log_section
from src.shared.tee_logger import enable_tee_logging

enable_tee_logging(LOCAL_LOG_PATH)


def main(argv=None):
    with log_section("🚀 Preview Generator"):
        log.info("✅ Preview Generator started.")
        parser = argparse.ArgumentParser(description="Factorio map preview generator")
        parser.add_argument(
            "map_string", help="Map exchange string to generate preview for"
        )
        args = parser.parse_args(argv)
        log.info("✅ Parsing complete")

        generate_previews_from_map_string(args.map_string)
        log.info("✅ Preview Generator completed successfully.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        log.exception("❌ Preview Generator failed with an exception.")
        raise
    finally:
        log.info("👋 Preview Generator exited.")
