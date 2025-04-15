import argparse
from pathlib import Path
from typing import Sequence

from pydantic import BaseModel, field_validator

from src.FactorioPreviewToolkit.preview_generator.exchange_string_to_settings import (
    convert_exchange_string_to_settings,
)
from src.FactorioPreviewToolkit.preview_generator.settings_to_map_previews import (
    generate_previews_from_settings,
)
from src.FactorioPreviewToolkit.shared.structured_logger import log, log_section
from src.FactorioPreviewToolkit.shared.utils import is_valid_map_string


class Args(BaseModel):
    factorio_path: Path
    map_string: str

    @field_validator("factorio_path")
    def check_factorio_path(cls, v: Path) -> Path:
        # Resolve relative path to absolute path
        v = v.resolve()

        # Check if the path exists and is a valid file (not a directory)
        if not v.exists() or not v.is_file():
            raise ValueError(f"Factorio path is invalid or does not exist: {v}")
        return v

    @field_validator("map_string")
    def check_map_string(cls, v: str) -> str:
        if not is_valid_map_string(v):
            raise ValueError(f"Invalid map exchange string: {v}")
        return v


def parse_arguments(argv: Sequence[str] | None = None) -> Args:
    parser = argparse.ArgumentParser(description="Factorio map preview generator")
    parser.add_argument("factorio_path", type=Path, help="Path to Factorio installation directory")
    parser.add_argument("map_string", type=str, help="Map exchange string to generate preview for")
    args = parser.parse_args(argv)

    return Args(**vars(args))


def main(argv: Sequence[str] | None = None) -> None:
    with log_section("🚀 Preview Generator started. Processing map string..."):
        arguments = parse_arguments(argv)
        convert_exchange_string_to_settings(arguments.factorio_path, arguments.map_string)
        generate_previews_from_settings(arguments.factorio_path)
        log.info("✅ Preview Generator completed successfully.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        log.exception("❌ Preview Generator failed with an exception.")
        raise
    finally:
        log.info("👋 Preview Generator exited.")
