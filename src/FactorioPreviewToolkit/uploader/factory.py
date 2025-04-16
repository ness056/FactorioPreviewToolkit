from src.FactorioPreviewToolkit.shared.config import Config
from src.FactorioPreviewToolkit.uploader.base_uploader import BaseUploader
from src.FactorioPreviewToolkit.uploader.rclone_uploader import RcloneUploader


def get_uploader() -> BaseUploader:
    """
    Returns the configured uploader instance based on the upload_method in config.
    Raises an error if the method is unsupported or disabled.
    """
    match Config.get().upload_method:
        case "rclone":
            return RcloneUploader()
        case "none":
            raise RuntimeError("Upload method is set to 'none'. Cannot upload.")
        case other:
            raise ValueError(f"Unsupported upload method: {other}")
