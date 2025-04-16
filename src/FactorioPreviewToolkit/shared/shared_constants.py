import textwrap
from pathlib import Path

from src.FactorioPreviewToolkit.shared.utils import get_project_root


class Constants:
    """
    Central definition of constants like directory and file paths used by the toolkit.
    Some directories are created on import to ensure availability.
    """

    # Common base directories
    BASE_PROJECT_DIR = get_project_root()
    BASE_TEMP_DIR = BASE_PROJECT_DIR / "temp_files"
    BASE_TEMP_DIR.mkdir(parents=True, exist_ok=True)  # Create directories if they don't exist

    LOG_DIR = BASE_PROJECT_DIR / "logs"
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    PREVIEW_TOOLKIT_CONFIG_PATH = BASE_PROJECT_DIR / "config.ini"
    BASE_ASSETS_DIR = BASE_PROJECT_DIR / "assets"
    FACTORIO_WRITE_DATA_PATH = BASE_TEMP_DIR / "data"
    FACTORIO_LOCK_PATH = FACTORIO_WRITE_DATA_PATH / ".lock"
    DUMMY_SAVE_TO_CREATE_MAP_GEN_SETTINGS_PATH = (
        BASE_TEMP_DIR / "dummy-save-to-create-map-gen-settings"
    )
    CONTROL_LUA_PATH = DUMMY_SAVE_TO_CREATE_MAP_GEN_SETTINGS_PATH / "control.lua"
    SCRIPT_OUTPUT_DIR = BASE_TEMP_DIR / "data" / "script-output"
    COMBINED_MAP_GEN_SETTINGS_FILENAME = "combined-map-gen-settings.json"
    COMBINED_MAP_GEN_SETTINGS_PATH = SCRIPT_OUTPUT_DIR / COMBINED_MAP_GEN_SETTINGS_FILENAME
    MAP_GEN_SETTINGS_PATH = BASE_TEMP_DIR / "map-gen-settings.json"
    LINK_OUTPUT_FILENAME = "output_links.txt"
    FACTORIO_CONFIG_FILENAME = "factorio_config.ini"

    @property
    def FACTORIO_CONFIG_PATH(self) -> Path:
        """
        Lazily initializes the Factorio config file path. If the file doesn't exist, it creates it with default content.
        """
        from src.FactorioPreviewToolkit.shared.structured_logger import log_section, log

        config_path = self.BASE_TEMP_DIR / self.FACTORIO_CONFIG_FILENAME
        if not config_path.exists():
            with log_section(f"❌ Factorio config not found at {config_path}. Creating it..."):
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


constants = Constants()
