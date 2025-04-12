from configparser import ConfigParser, ExtendedInterpolation
from typing import Union

from src.shared.config_schema import Settings
from src.shared.structured_logger import log, log_section


class Config:
    _instance: Settings | None = None
    _path: str = "config.ini"

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
            parser = ConfigParser(interpolation=ExtendedInterpolation())
            parser.read(cls._path)

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
