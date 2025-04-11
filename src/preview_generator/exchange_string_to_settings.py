import json
import re
import textwrap
import zipfile
from pathlib import Path

from src.preview_generator.factorio_interface import run_factorio_command
from src.shared.config import Config
from src.shared.shared_constants import constants
from src.shared.structured_logger import log, log_section


def _build_control_lua(exchange_string: str, output_filename: str) -> str:
    return textwrap.dedent(
        f"""
        script.on_event(defines.events.on_tick, function(event)
            if event.tick == 0 then
                local exchange_string = "{exchange_string}"
                local json = helpers.table_to_json(helpers.parse_map_exchange_string(exchange_string))
                helpers.write_file("{output_filename}", json)
            end
        end)
    """
    ).strip()


def _create_dummy_save(factorio_path: Path) -> None:
    with log_section("🛠️ Creating dummy save..."):
        save_folder = constants.DUMMY_SAVE_TO_CREATE_MAP_GEN_SETTINGS_PATH

        if save_folder.exists():
            log.info(f"✅ Dummy save already exists at: {save_folder}")
            return

        log.info(f"📦 Creating dummy save at: {save_folder}")
        save_zip = save_folder.with_suffix(".zip")
        run_factorio_command(factorio_path, ["--create", str(save_zip)])

        log.info("📂 Extracting dummy save zip.")
        with zipfile.ZipFile(save_zip, "r") as zip_ref:
            zip_ref.extractall(save_folder.parent)
        save_zip.unlink()
        log.info("✅ Dummy save created.")


def _update_control_lua(save_folder: Path, exchange_string: str) -> None:
    with log_section("🛠️ Updating control.lua with exchange string..."):
        control_lua = constants.CONTROL_LUA_PATH
        if not control_lua.exists():
            raise FileNotFoundError(f"❌ control.lua not found: {control_lua}")

        original = control_lua.read_text(encoding="utf-8")

        cleaned = re.sub(
            r"script\.on_event\(defines\.events\.on_tick, function\(event\).*?>>>.*?<<<.*?end\s*end\)",
            "",
            original,
            flags=re.DOTALL,
        ).strip()

        injected_exchange_handler = _build_control_lua(
            exchange_string, constants.COMBINED_MAP_GEN_SETTINGS_FILENAME
        )

        result = cleaned + "\n\n" + injected_exchange_handler + "\n"
        if result != original:
            control_lua.write_text(result, encoding="utf-8")
            log.info("✅ control.lua updated.")
        else:
            log.info("✅ control.lua already up to date.")


def _extract_map_gen_settings_from_combined_json(script_output_path: Path) -> None:
    with log_section("📤 Extracting map-gen-settings from combined JSON..."):
        combined_path = constants.COMBINED_MAP_GEN_SETTINGS_PATH
        if not combined_path.exists():
            raise FileNotFoundError(
                f"❌ Combined settings file not found: {combined_path}"
            )

        with combined_path.open("r", encoding="utf-8") as f:
            combined_data = json.load(f)

        map_gen_settings = combined_data.get("map_gen_settings")
        if not map_gen_settings:
            raise ValueError(
                "❌ 'map_gen_settings' key missing in combined settings JSON."
            )

        output_path = Path(constants.MAP_GEN_SETTINGS_PATH)
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(map_gen_settings, f, indent=2)

        log.info(f"✅ Extracted to {constants.MAP_GEN_SETTINGS_PATH}")


def _export_map_gen_settings_via_benchmark(
    factorio_path: Path, save_folder: Path
) -> None:
    with log_section("🧪 Running Factorio to export map-gen-settings..."):
        run_factorio_command(
            factorio_path,
            [
                "--benchmark",
                str(save_folder),
                "-ticks",
                "1",
            ],
        )
        log.info("✅ Map-gen-setting exported successfully.")


def convert_exchange_string_to_settings(factorio_path: Path, map_string: str) -> None:
    with log_section("🧩 Converting map exchange string to map-gen-settings..."):
        _create_dummy_save(factorio_path)
        _update_control_lua(
            constants.DUMMY_SAVE_TO_CREATE_MAP_GEN_SETTINGS_PATH, map_string
        )
        _export_map_gen_settings_via_benchmark(
            factorio_path, constants.DUMMY_SAVE_TO_CREATE_MAP_GEN_SETTINGS_PATH
        )
        _extract_map_gen_settings_from_combined_json(
            Config.get().previews_output_folder
        )
        log.info("✅ Map-gen-settings extracted.")
