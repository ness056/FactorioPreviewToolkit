import sys
from pathlib import Path
from typing import Optional, List

from pydantic import BaseModel, field_validator, model_validator


class Settings(BaseModel):
    # === Factorio Location ===
    factorio_locator_method: str  # fixed_path or active_window
    factorio_folder: Optional[Path] = None  # Required only for fixed_path
    factorio_executable: Optional[Path] = None

    # === Script Output and Previews ===
    script_output_folder: Path
    map_preview_size: int
    previews_output_folder: Path
    planet_names: List[str]

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
    upload_method: str
    rclone_folder: Path
    rclone_remote_service: str
    upload_remote_folder: Path
    rclone_executable: Optional[Path] = None

    # === Validators ===

    @field_validator("map_preview_size")
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("map_preview_size must be a positive integer")
        return v

    @field_validator(
        "sound_volume_start_file",
        "sound_volume_success_file",
        "sound_volume_failure_file",
    )
    def volumes_between_0_and_1(cls, v, info):
        if not (0.0 <= v <= 1.0):
            raise ValueError(f"{info.field_name} must be between 0.0 and 1.0")
        return v

    @field_validator(
        "sound_start_file",
        "sound_success_file",
        "sound_failure_file",
        "previews_output_folder",
        "rclone_folder",
    )
    def path_must_exist(cls, v: Path, info):
        if not v.exists():
            raise ValueError(f"{info.field_name} does not exist: {v}")
        return v.resolve()

    @model_validator(mode="after")
    def validate_if_required(self):
        method = self.factorio_locator_method
        if method == "fixed_path":
            if not self.factorio_folder:
                raise ValueError("factorio_folder must be set when using 'fixed_path'")
        return self

    @field_validator("planet_names")
    def planets_cannot_be_empty(cls, v):
        if not v:
            raise ValueError("planet_names cannot be empty")
        return v

    @field_validator("upload_method")
    def check_upload_method(cls, v):
        if v not in ("rclone", "none"):
            raise ValueError("upload_method must be 'rclone' or 'none'")
        return v

    @field_validator("map_exchange_input_method")
    def validate_map_method(cls, v):
        valid = {"clipboard_auto", "clipboard_hotkey", "file_hotkey", "dialog_hotkey"}
        if v not in valid:
            raise ValueError(f"Invalid map_exchange_input_method: {v}")
        return v

    @field_validator("factorio_locator_method")
    def validate_locator_method(cls, v):
        if v == "config":
            return "fixed_path"
        if v not in {"fixed_path", "active_window"}:
            raise ValueError(
                "factorio_locator_method must be 'fixed_path' or 'active_window'"
            )
        return v

    @model_validator(mode="after")
    def resolve_executables(self):
        # Factorio: only resolve for fixed_path
        if self.factorio_locator_method == "fixed_path":
            folder = self.factorio_folder
            if not folder:
                raise ValueError("factorio_folder is missing for fixed_path")

            if sys.platform.startswith("win"):
                exe = folder / "bin" / "x64" / "factorio.exe"
            elif sys.platform.startswith("darwin"):
                if folder.is_dir() and (folder / "Factorio.app").exists():
                    folder = folder / "Factorio.app"
                exe = (
                    folder / "Contents" / "MacOS" / "factorio"
                    if folder.name.endswith(".app")
                    else folder / "bin" / "x64" / "factorio"
                )
            elif sys.platform.startswith("linux"):
                exe = folder / "bin" / "x64" / "factorio"
            else:
                raise RuntimeError("Unsupported platform.")

            if not exe.exists():
                raise ValueError(f"Factorio executable not found: {exe}")
            self.factorio_executable = exe

        # Rclone: always resolve
        name = "rclone.exe" if sys.platform.startswith("win") else "rclone"
        rclone_exec = self.rclone_folder / name
        if not rclone_exec.exists():
            raise ValueError(f"rclone executable not found: {rclone_exec}")
        self.rclone_executable = rclone_exec

        return self
