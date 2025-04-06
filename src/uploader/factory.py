from src.shared.config_loader import get_config
from src.uploader.base_uploader import BaseUploader
from src.uploader.rclone_uploader import RcloneUploader


def get_uploader() -> BaseUploader:
    match get_config().upload_method:
        case "rclone":
            return RcloneUploader()
        case "none":
            raise RuntimeError("Upload method is set to 'none'. Cannot upload.")
        case other:
            raise ValueError(f"Unsupported upload method: {other}")
