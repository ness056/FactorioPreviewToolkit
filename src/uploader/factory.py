from src.shared.config import Config
from src.uploader.base_uploader import BaseUploader
from src.uploader.rclone_uploader import RcloneUploader


def get_uploader() -> BaseUploader:
    match Config.get().upload_method:
        case "rclone":
            return RcloneUploader()
        case "none":
            raise RuntimeError("Upload method is set to 'none'. Cannot upload.")
        case other:
            raise ValueError(f"Unsupported upload method: {other}")
