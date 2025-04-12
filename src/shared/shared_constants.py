import textwrap
from pathlib import Path

from src.shared.config import Config
from src.shared.structured_logger import log_section, log


class Constants:
    # Common base directories
    BASE_TEMP_DIR = Path("./temp_files")
    BASE_TEMP_DIR.mkdir(
        parents=True, exist_ok=True
    )  # Create directories if they don't exist
    BASE_ASSETS_DIR = Path("./assets")

    # Subdirectories under base directories
    FACTORIO_WRITE_DATA_PATH = BASE_TEMP_DIR / "data"
    FACTORIO_LOCK_PATH = FACTORIO_WRITE_DATA_PATH / ".lock"
    DUMMY_SAVE_DIR = BASE_TEMP_DIR / "dummy-save-to-create-map-gen-settings"
    CONTROL_LUA_PATH = DUMMY_SAVE_DIR / "control.lua"
    SCRIPT_OUTPUT_DIR = BASE_TEMP_DIR / "data" / "script-output"

    # Specific paths using the common base variables
    DUMMY_SAVE_TO_CREATE_MAP_GEN_SETTINGS_PATH = DUMMY_SAVE_DIR
    COMBINED_MAP_GEN_SETTINGS_FILENAME = "combined-map-gen-settings.json"
    COMBINED_MAP_GEN_SETTINGS_PATH = (
        SCRIPT_OUTPUT_DIR / COMBINED_MAP_GEN_SETTINGS_FILENAME
    )
    MAP_GEN_SETTINGS_PATH = BASE_TEMP_DIR / "map-gen-settings.json"

    def __init__(self) -> None:
        self._link_output_path: Path | None = None

    @property
    def FACTORIO_CONFIG_PATH(self) -> Path:
        """
        Lazily initializes the Factorio config file path. If the file doesn't exist, it creates it with default content.
        """
        config_path = self.BASE_TEMP_DIR / "factorio_config.ini"
        if not config_path.exists():
            with log_section(
                f"❌ Factorio config not found at {config_path}. Creating it..."
            ):
                config_content = textwrap.dedent(
                    f"""
                    ; version=12
                    [path]
                    read-data=__PATH__executable__/../../data
                    write-data={self.FACTORIO_WRITE_DATA_PATH}
                    """
                )
                with open(config_path, "w") as config_file:
                    config_file.write(config_content)
                log.info("✅ Factorio config created.")
        return config_path

    @property
    def LINK_OUTPUT_PATH(self) -> Path:
        """
        Lazily loads the LINK_OUTPUT_PATH from the config if set,
        otherwise raises an error if not defined.
        """
        if self._link_output_path is None:
            config = Config.get()
            self._link_output_path = (
                Path(config.previews_output_folder) / "output_links.txt"
            )
        return self._link_output_path


constants = Constants()
