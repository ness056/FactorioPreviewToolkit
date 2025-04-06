import json
import re
import zipfile
from pathlib import Path

from src.preview_generator.factorio_interface import run_factorio_command
from src.shared.config_loader import get_config
from src.shared.shared_constants import (
    map_gen_settings_filename,
    dummy_save_to_create_map_gen_settings,
    combined_settings_output_filename,
)
from src.shared.structured_logger import log


def _is_valid_exchange_string(s: str) -> bool:
    return bool(re.match(r"^>>>eN[a-zA-Z0-9+/=]+<<<$", s.strip()))


def _ensure_dummy_save_exists(save_folder: Path) -> None:
    if save_folder.exists():
        log.info(f"📁 Dummy save already exists at: {save_folder}")
        return

    log.info(f"📦 Creating dummy save at: {save_folder}")
    save_zip = save_folder.with_suffix(".zip")
    run_factorio_command(["--create", str(save_zip)])

    log.info("📂 Extracting dummy save zip...")
    with zipfile.ZipFile(save_zip, "r") as zip_ref:
        zip_ref.extractall()
    save_zip.unlink()


def _update_control_lua(save_folder: Path, exchange_string: str) -> None:
    log.info("🛠️ Updating control.lua with exchange string...")
    control_lua = save_folder / "control.lua"
    if not control_lua.exists():
        raise FileNotFoundError(f"❌ control.lua not found: {control_lua}")

    original = control_lua.read_text(encoding="utf-8")

    cleaned = re.sub(
        r"script\.on_event\(defines\.events\.on_tick, function\(event\).*?>>>.*?<<<.*?end\s*end\)",
        "",
        original,
        flags=re.DOTALL,
    ).strip()

    logic = f"""
script.on_event(defines.events.on_tick, function(event)
    if event.tick == 0 then
        local exchange_string = "{exchange_string}"
        local json = helpers.table_to_json(helpers.parse_map_exchange_string(exchange_string))
        helpers.write_file("{combined_settings_output_filename}", json)
        game.print("Map settings exported to {combined_settings_output_filename}")
    end
end)
""".strip()

    result = cleaned + "\n\n" + logic + "\n"
    if result != original:
        control_lua.write_text(result, encoding="utf-8")
        log.info("✅ control.lua updated.")
    else:
        log.info("⚠️ No changes made to control.lua.")


def _extract_map_gen_settings_from_combined_json(script_output_path: Path) -> None:
    combined_path = script_output_path / combined_settings_output_filename
    if not combined_path.exists():
        raise FileNotFoundError(f"❌ Combined settings file not found: {combined_path}")

    with combined_path.open("r", encoding="utf-8") as f:
        combined_data = json.load(f)

    map_gen_settings = combined_data.get("map_gen_settings")
    if not map_gen_settings:
        raise ValueError("❌ 'map_gen_settings' key missing in combined settings JSON.")

    output_path = Path(map_gen_settings_filename)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(map_gen_settings, f, indent=2)

    log.info(f"✅ Extracted map_gen_settings to {map_gen_settings_filename}")


def convert_exchange_string_to_settings(map_string: str) -> None:
    if not _is_valid_exchange_string(map_string):
        raise ValueError("Invalid map exchange string.")

    save_folder = Path(dummy_save_to_create_map_gen_settings)
    _ensure_dummy_save_exists(save_folder)
    _update_control_lua(save_folder, map_string)

    run_factorio_command(["--benchmark", str(save_folder), "-ticks", "1"])

    config = get_config()
    _extract_map_gen_settings_from_combined_json(config.script_output_folder)
