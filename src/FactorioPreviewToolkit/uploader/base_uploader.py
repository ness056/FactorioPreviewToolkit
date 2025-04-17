from abc import ABC, abstractmethod
from pathlib import Path

from src.FactorioPreviewToolkit.shared.config import Config
from src.FactorioPreviewToolkit.shared.structured_logger import log, log_section


def _write_links_file(planet_links: dict[str, str]) -> None:
    """
    Writes a summary file with links to each uploaded image, one per planet.
    """
    with log_section("📝 Saving download links to file..."):
        config = Config.get()
        try:
            with config.preview_output_file.open("w", encoding="utf-8") as f:
                for planet, url in planet_links.items():
                    f.write(f"{planet}: {url}\n")
            log.info(f"✅ Download links saved to: {config.preview_output_file}")
        except Exception:
            log.error(f"❌ Failed to write output file: {config.preview_output_file}")
            raise


class BaseUploader(ABC):
    """
    Abstract uploader class. Handles upload of all planet preview images.
    Subclasses must implement upload_single().
    """

    def upload_all(self) -> None:
        """
        Uploads all planet preview images and saves the resulting download links to a file.
        """
        config = Config.get()
        with log_section("🚀 Starting image upload..."):
            planet_links: dict[str, str] = {}

            for planet in config.planet_names:
                with log_section(f"🌍 Uploading {planet.capitalize()}..."):
                    image_path = config.previews_output_dir / f"{planet}.png"
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
    def upload_single(self, local_path: Path, remote_filename: str) -> str:
        """
        Uploads a single image file and returns a public URL.
        """
        ...
