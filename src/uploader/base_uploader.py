from abc import ABC, abstractmethod
from pathlib import Path

from src.shared.config import Config
from src.shared.shared_constants import constants
from src.shared.structured_logger import log, log_section


def _write_links_file(planet_links: dict[str, str]) -> None:
    with log_section("📝 Saving download links to file..."):
        try:
            with constants.LINK_OUTPUT_PATH.open("w", encoding="utf-8") as f:
                for planet, url in planet_links.items():
                    f.write(f"{planet}: {url}\n")
            log.info(f"✅ Download links saved to: {constants.LINK_OUTPUT_PATH}")
        except Exception:
            log.error(f"❌ Failed to write output file: {constants.LINK_OUTPUT_PATH}")
            raise


class BaseUploader(ABC):
    def upload_all(self) -> None:
        config = Config.get()
        with log_section("🚀 Starting image upload..."):
            planet_links: dict[str, str] = {}

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

            _write_links_file(planet_links)
            log.info("✅ All uploads complete.")

    @abstractmethod
    def upload_single(self, local_path: Path, remote_filename: str) -> str: ...
