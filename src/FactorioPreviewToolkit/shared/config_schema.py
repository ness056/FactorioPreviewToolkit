import sys
from pathlib import Path
from typing import Literal, Any

from pydantic import BaseModel, field_validator, model_validator
from pydantic_core.core_schema import FieldValidationInfo

from src.FactorioPreviewToolkit.shared.shared_constants import constants
from src.FactorioPreviewToolkit.shared.utils import resolve_relative_to_project_root


class Settings(BaseModel):
    # === Factorio Location ===
    factorio_locator_method: Literal["fixed_path", "active_window"]
    fixed_path_factorio_executable: Path | None = None  # Path to Factorio executable
    active_window_poll_interval_in_seconds: int = 2

    # === Script Output and Previews ===
    map_preview_size: int
    previews_output_folder: Path
    preview_output_file: Path  # Computed from previews_output_folder
    planet_names: list[str]

    # === Sound Settings ===
    sound_start_file: Path
    sound_volume_start_file: float
    sound_success_file: Path
    sound_volume_success_file: float
    sound_failure_file: Path
    sound_volume_failure_file: float

    # === Map Exchange Input ===
    map_exchange_input_method: str
    map_exchange_file_path: Path

    # === Upload Settings ===
    upload_method: Literal["rclone", "none"]
    rclone_folder: Path
    rclone_remote_service: str
    upload_remote_folder: Path
    rclone_executable: Path | None = None  # Auto-resolved from rclone_folder

    class Config:
        frozen = True

    @model_validator(mode="before")
    def resolve_paths_relative_to_project_root(cls, values: dict[str, Any]) -> dict[str, Any]:

        def resolve(name: str) -> None:
            if values.get(name) is not None:
                values[name] = resolve_relative_to_project_root(values[name])

        # Resolve all user-defined paths
        resolve("fixed_path_factorio_executable")
        resolve("previews_output_folder")
        resolve("sound_start_file")
        resolve("sound_success_file")
        resolve("sound_failure_file")
        resolve("map_exchange_file_path")
        resolve("rclone_folder")
        resolve("upload_remote_folder")
        resolve("rclone_executable")

        if "previews_output_folder" in values:
            resolved_preview_folder = resolve_relative_to_project_root(
                values["previews_output_folder"]
            )
            values["preview_output_file"] = resolved_preview_folder / constants.LINK_OUTPUT_FILENAME

        raw_folder = values.get("rclone_folder")
        if raw_folder is not None:
            rclone_folder = Path(raw_folder)
            name = "rclone.exe" if sys.platform.startswith("win") else "rclone"
            values["rclone_executable"] = rclone_folder / name

        return values

    # === Validators ===

    @field_validator("map_preview_size")
    def must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("map_preview_size must be a positive integer")
        return v

    @field_validator(
        "sound_volume_start_file",
        "sound_volume_success_file",
        "sound_volume_failure_file",
    )
    def volumes_between_0_and_1(cls, v: float, info: FieldValidationInfo) -> float:
        if not (0.0 <= v <= 1.0):
            # Access alias directly from info.data
            alias = info.data.get(
                "alias", "unknown field"
            )  # Default to 'unknown field' if alias not found
            raise ValueError(f"{alias} must be between 0.0 and 1.0")
        return v

    @field_validator(
        "sound_start_file",
        "sound_success_file",
        "sound_failure_file",
        "previews_output_folder",
        "rclone_folder",
    )
    def path_must_exist(cls, v: Path, info: FieldValidationInfo) -> Path:
        if not v.exists():
            # Accessing the alias via the field's metadata (through info.data)
            alias = info.data.get(
                "alias", "unknown field"
            )  # Default to 'unknown field' if alias is not found
            raise ValueError(f"{alias} does not exist: {v}")
        return v.resolve()

    @field_validator("rclone_executable")
    def check_rclone_executable_exists(
        cls, v: Path | None, info: FieldValidationInfo
    ) -> Path | None:
        if info.data.get("upload_method") == "rclone":
            if not v or not v.exists():
                raise ValueError(f"rclone executable not found at {v}")
        return v

    @field_validator("fixed_path_factorio_executable")
    def check_factorio_executable_exists(
        cls, v: Path | None, info: FieldValidationInfo
    ) -> Path | None:
        if info.data.get("factorio_locator_method") == "fixed_path" and v and not v.exists():
            raise ValueError(f"Factorio executable not found at {v}")
        return v

    @field_validator("active_window_poll_interval_in_seconds")
    def check_poll_interval_if_active_window(cls, v: int, info: FieldValidationInfo) -> int:
        if info.data.get("factorio_locator_method") == "active_window" and v <= 0:
            raise ValueError(
                "active_window_poll_interval_in_seconds must be > 0 for active_window mode"
            )
        return v

    @field_validator("planet_names")
    def planets_cannot_be_empty(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("planet_names cannot be empty")
        return v

    @field_validator("upload_method")
    def check_upload_method(cls, v: str) -> str:
        if v not in ("rclone", "none"):
            raise ValueError("upload_method must be 'rclone' or 'none'")
        return v

    @field_validator("map_exchange_input_method")
    def validate_map_method(cls, v: str) -> str:
        valid = {"clipboard_auto", "clipboard_hotkey", "file_hotkey", "dialog_hotkey"}
        if v not in valid:
            raise ValueError(f"Invalid map_exchange_input_method: {v}")
        return v

    @field_validator("factorio_locator_method")
    def validate_locator_method(cls, v: str) -> str:
        if v not in {"fixed_path", "active_window"}:
            raise ValueError("factorio_locator_method must be 'fixed_path' or 'active_window'")
        return v
