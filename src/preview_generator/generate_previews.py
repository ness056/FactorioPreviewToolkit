from src.preview_generator.exchange_string_to_settings import (
    convert_exchange_string_to_settings,
)
from src.preview_generator.settings_to_map_previews import (
    generate_previews_from_settings,
)
from src.shared.config_loader import get_config
from src.shared.structured_logger import log


def generate_previews_from_map_string(map_string: str) -> None:
    log.info("🛰️ Generating map previews from map exchange string...")
    config = get_config()
    convert_exchange_string_to_settings(map_string)
    generate_previews_from_settings(
        factorio_path=config.factorio_folder, preview_width=config.map_preview_size
    )

    log.info("✅ Preview generation complete.")
