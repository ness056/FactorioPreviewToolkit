import json
from abc import ABC, abstractmethod
from pathlib import Path

from src.FactorioPreviewToolkit.shared.shared_constants import Constants
from src.FactorioPreviewToolkit.shared.structured_logger import log, log_section


def _write_links_file(planet_links: dict[str, str]) -> None:
    """
    Writes a JavaScript config object with links to each uploaded image, one per planet.
    """
    with log_section("📝 Saving download links to file..."):
        preview_links_filepath = Constants.PREVIEW_LINKS_FILEPATH
        try:
            with preview_links_filepath.open("w", encoding="utf-8") as f:
                f.write("const planetConfig = {\n")
                for planet, url in planet_links.items():
                    f.write(f'  {planet}: "{url}",\n')
                f.write("};\n")
            log.info(f"✅ Download links saved to: {preview_links_filepath}")
        except Exception:
            log.error(f"❌ Failed to write output file: {preview_links_filepath}")
            raise


def _load_planet_names() -> list[str]:
    """
    Loads the list of planet names from the JSON file generated during preview setup.
    """
    planet_file = Constants.PLANET_NAMES_OUTPUT_FILEPATH
    with log_section("📄 Loading planet names..."):
        try:
            with planet_file.open("r", encoding="utf-8") as f:
                planets = json.load(f)
            if not isinstance(planets, list) or not all(isinstance(p, str) for p in planets):
                raise ValueError("Invalid format in planet list JSON.")
            log.info(f"✅ Loaded {len(planets)} planets: {', '.join(planets)}")
            return planets
        except Exception:
            log.error("❌ Failed to load or parse planet names file.")
            raise


class BaseUploader(ABC):
    """
    Abstract uploader class. Uploads the planet names file and all planet preview images.
    Subclasses must implement upload_single().
    """

    def upload_all(self) -> None:
        """
        Uploads the planet names file and all preview images listed in it.
        Saves resulting download links to a JavaScript config file.
        """
        with log_section("🚀 Uploading preview assets..."):
            planet_names = _load_planet_names()
            self._upload_planet_names_file()
            planet_links = self._upload_planet_images(planet_names)
            _write_links_file(planet_links)
            log.info("✅ All assets uploaded successfully.")

    def _upload_planet_names_file(self) -> None:
        """
        Uploads the planet names JSON file itself.
        """
        with log_section("📤 Uploading planet names file..."):
            try:
                self.upload_single(
                    Constants.PLANET_NAMES_OUTPUT_FILEPATH, Constants.PLANET_NAMES_FILENAME
                )
                log.info("✅ Planet names uploaded.")
            except Exception:
                log.error("❌ Failed to upload planet names.")
                raise

    def _upload_planet_images(self, planet_names: list[str]) -> dict[str, str]:
        """
        Uploads all preview images and returns a dict of download links.
        """
        links: dict[str, str] = {}

        for planet in planet_names:
            with log_section(f"🌍 Uploading {planet} preview..."):
                image_path = Constants.PREVIEWS_OUTPUT_DIR / f"{planet}.png"
                try:
                    url = self.upload_single(image_path, f"{planet}.png")
                    links[planet] = url
                    log.info(f"✅ {planet} uploaded.")
                except Exception:
                    log.error(f"❌ Failed to upload {planet}.png")
                    raise

        return links

    @abstractmethod
    def upload_single(self, local_path: Path, remote_filename: str) -> str:
        """
        Uploads a single file and returns a public URL.
        """
        ...
