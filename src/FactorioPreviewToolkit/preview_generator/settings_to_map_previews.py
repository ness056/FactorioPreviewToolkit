import json
from pathlib import Path

from src.FactorioPreviewToolkit.preview_generator.factorio_interface import run_factorio_command
from src.FactorioPreviewToolkit.shared.config import Config
from src.FactorioPreviewToolkit.shared.shared_constants import constants
from src.FactorioPreviewToolkit.shared.structured_logger import log, log_section


def _extract_seed(settings_path: Path) -> int:
    """
    Loads and validates the seed from the given map-gen-settings file.
    """
    with log_section("🌱 Extracting seed from map-gen-settings..."):
        try:
            with settings_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                seed = data["seed"]
                if not isinstance(seed, int):
                    raise ValueError
        except Exception:
            log.error("❌ Invalid or missing seed in map-gen-settings.")
            raise

        log.info(f"✅ Seed extracted: {seed}")
        return seed


def prepare_preview_generation() -> tuple[Path, int]:
    """
    Validates the seed and loads the preview width from config.
    """
    settings_path = Path(constants.MAP_GEN_SETTINGS_FILEPATH)
    _extract_seed(settings_path)
    preview_width = Config.get().map_preview_size
    return settings_path, preview_width


def generate_planet_previews(
    factorio_base_path: Path, settings_path: Path, preview_width: int
) -> None:
    """
    Runs preview generation for all planets configured in the config.
    """
    planet_names = Config.get().planet_names

    for planet in planet_names:
        with log_section(f"🪐 Generating preview for {planet}..."):
            try:
                _generate_preview_for_planet(
                    factorio_base_path, planet, settings_path, preview_width
                )
            except Exception:
                log.error(f"❌ Failed to generate preview for {planet}")
                raise


def _generate_preview_for_planet(
    factorio_base_path: Path, planet: str, settings_path: Path, preview_width: int
) -> None:
    """
    Generates a single preview image for one planet using Factorio CLI.
    """
    output = Config.get().previews_output_dir / f"{planet}.png"

    args = [
        f"--generate-map-preview={output}",
        f"--map-gen-settings={settings_path}",
        f"--map-preview-size={preview_width}",
        f"--map-preview-planet={planet}",
    ]

    run_factorio_command(factorio_base_path, args)
    log.info(f"✅ Preview generated at {output}")


def generate_previews_from_settings(factorio_base_path: Path) -> None:
    """
    Main entry point: validates settings and triggers preview generation for all planets.
    """
    with log_section("🌍 Starting map preview generation..."):
        settings_path, preview_width = prepare_preview_generation()
        generate_planet_previews(factorio_base_path, settings_path, preview_width)
        log.info("✅ All planet previews generated successfully.")
