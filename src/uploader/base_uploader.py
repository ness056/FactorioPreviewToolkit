from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict

from src.shared.config_loader import get_config
from src.shared.structured_logger import log, log_section
from src.uploader.constants import LINK_OUTPUT_FILE


class BaseUploader(ABC):
    def upload_all(self) -> None:
        config = get_config()
        with log_section("🚀 Starting image upload..."):
            planet_links: Dict[str, str] = {}

            for planet in config.planet_names:
                with log_section(f"🌍 Uploading {planet.capitalize()}..."):
                    image_path = config.previews_output_folder / f"{planet}.png"
                    try:
                        link = self.upload_single(image_path, f"{planet}.png")
                        planet_links[planet] = link
                        log.info(f"✅ {planet.capitalize()} done.")
                    except Exception:
                        log.error(f"❌ Failed to upload {planet}.png")
                        raise

            self._write_links_file(planet_links)
            log.info("✅ All uploads complete.")

    def _write_links_file(self, planet_links: Dict[str, str]) -> None:
        with log_section("📝 Saving download links to file..."):
            try:
                with LINK_OUTPUT_FILE.open("w", encoding="utf-8") as f:
                    for planet, url in planet_links.items():
                        f.write(f"{planet}: {url}\n")
                log.info(f"✅ Download links saved to: {LINK_OUTPUT_FILE}")
            except Exception:
                log.error(f"❌ Failed to write output file: {LINK_OUTPUT_FILE}")
                raise

    @abstractmethod
    def upload_single(self, local_path: Path, remote_filename: str) -> str: ...
