from configparser import ConfigParser, ExtendedInterpolation

from src.shared.config_schema import Settings
from src.shared.structured_logger import log, log_section

_config_instance: Settings | None = None


def set_config(config: Settings) -> None:
    global _config_instance
    if _config_instance is not None:
        raise RuntimeError("Config already set.")
    _config_instance = config


def get_config() -> Settings:
    if _config_instance is None:
        raise RuntimeError("Config not set.")
    return _config_instance


def _load_and_set_config() -> None:
    log_section("🔍 Reading config...")

    parser = ConfigParser(interpolation=ExtendedInterpolation())
    parser.read("config.ini")

    data = {}

    def flat(section):
        return {k: v for k, v in parser[section].items()}

    data.update(flat("settings"))
    data.update(flat("map_exchange_input"))
    data.update(flat("upload"))

    # Convert stringified list into Python list
    data["planet_names"] = [
        x.strip(" '\"")
        for x in data["planet_names"].strip("[]").split(",")
        if x.strip()
    ]

    try:
        settings = Settings(**data)
        set_config(settings)
        log.info("✅ Config loaded and validated successfully.")
    except Exception as e:
        log.info(f"❌ Failed to load config: {e}")
        raise


# Auto-load config on import
_load_and_set_config()
