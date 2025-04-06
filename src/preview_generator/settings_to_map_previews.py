# src/preview_generator/settings_to_map_previews.py

import json
from pathlib import Path

from src.preview_generator.factorio_interface import run_factorio_command
from src.shared import shared_constants
from src.shared.config_loader import get_config
from src.shared.structured_logger import log


def _extract_seed(settings_path: Path) -> int:
    log.info("🔢 Extracting seed from map-gen-settings...")
    with settings_path.open("r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            seed = data["seed"]
            if not isinstance(seed, int):
                raise ValueError
        except Exception:
            log.error("❌ Invalid or missing seed in map-gen-settings.")
            raise
    log.info(f"✅ Seed extracted: {seed}")
    return seed


def generate_previews_from_settings(factorio_path: Path, preview_width: int) -> None:
    log.info("🌍 Generating map previews...")
    config = get_config()
    settings_path = Path(shared_constants.map_gen_settings_filename)
    _extract_seed(settings_path)

    for planet in config.planet_names:
        output = config.previews_output_folder / f"{planet}.png"
        args = [
            f"--generate-map-preview={output}",
            f"--map-gen-settings={settings_path}",
            f"--map-preview-size={preview_width}",
            f"--map-preview-planet={planet}",
        ]

        try:
            run_factorio_command(args)
            log.info(f"✅ {planet.capitalize()} generated.")
        except Exception:
            log.error(f"❌ Failed to generate preview for {planet}")
            raise
