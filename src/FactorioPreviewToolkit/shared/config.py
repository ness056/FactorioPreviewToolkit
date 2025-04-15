from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path
from typing import Union

from src.FactorioPreviewToolkit.shared.config_schema import Settings
from src.FactorioPreviewToolkit.shared.shared_constants import constants
from src.FactorioPreviewToolkit.shared.structured_logger import log, log_section


class Config:
    _instance: Settings | None = None
    _path = Path(constants.PREVIEW_TOOLKIT_CONFIG_PATH)

    @classmethod
    def get(cls) -> Settings:
        if cls._instance is None:
            cls._load()
            if cls._instance is None:
                raise ValueError("Failed to load settings from config file.")
        return cls._instance

    @classmethod
    def _load(cls) -> None:
        with log_section("🔍 Initializing config..."):
            config_path = cls._path

            if not config_path.exists():
                log.error(f"❌ Config file not found at: {config_path}")
                raise FileNotFoundError(f"Config file not found at: {config_path}")

            parser = ConfigParser(interpolation=ExtendedInterpolation())
            parser.read(config_path)

            def flat(section_name: str) -> dict[str, str]:
                return {k: v for k, v in parser[section_name].items()}

            data: dict[str, Union[str, list[str]]] = {}
            data.update(flat("settings"))
            data.update(flat("map_exchange_input"))
            data.update(flat("upload"))

            # Convert stringified list into Python list
            data["planet_names"] = [
                x.strip(" '\"")
                for x in str(data["planet_names"]).strip("[]").split(",")
                if x.strip()
            ]

            try:
                # cls._instance = Settings(**data)
                cls._instance = Settings.model_validate(data)
                log.info("✅ Config loaded and validated successfully.")
            except Exception as e:
                log.error(f"❌ Failed to load config: {e}")
                raise
