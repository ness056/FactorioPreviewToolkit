import subprocess
from pathlib import Path

from src.shared.config import Config
from src.shared.structured_logger import log, log_section
from src.uploader.base_uploader import BaseUploader


class RcloneUploader(BaseUploader):

    def _is_rclone_configured(self, remote_name: str) -> bool:
        rclone = Config.get().rclone_executable
        result = subprocess.run([rclone, "listremotes"], capture_output=True, text=True)
        remotes = result.stdout.strip().splitlines()
        return any(remote_name + ":" == remote for remote in remotes)

    def _open_rclone_config(self) -> None:
        rclone = Config.get().rclone_executable
        log.info("🔧 Opening rclone config interface...")

        try:
            subprocess.run([rclone, "config"], check=True)
        except subprocess.CalledProcessError as e:
            log.error("❌ Failed to launch rclone config.")
            log.error(f"stdout:\n{e.stdout}")
            log.error(f"stderr:\n{e.stderr}")
            raise

    def upload_single(self, local_path: Path, remote_filename: str) -> str:
        config = Config.get()
        rclone = Config.get().rclone_executable
        remote_name = config.rclone_remote_service
        remote_folder = config.upload_remote_folder
        remote_target = f"{remote_name}:{remote_folder}"
        full_remote_path = f"{remote_target}/{remote_filename}"

        if not self._is_rclone_configured(remote_name):
            log.warning(f"⚠️ Rclone remote '{remote_name}' is not configured.")
            self._open_rclone_config()
            raise RuntimeError(f"Rclone remote '{remote_name}' not configured.")

        with log_section(f"⬆️ Uploading {local_path.name} to {remote_target}..."):
            try:
                result = subprocess.run(
                    [rclone, "copy", str(local_path), remote_target],
                    check=True,
                    capture_output=True,
                    text=True,
                )

                # Filter out known harmless notices
                for line in result.stderr.splitlines():
                    if "Forced to upload files to set modification times" not in line:
                        log.info(line)

                log.info("✅ Upload complete.")
            except subprocess.CalledProcessError as e:
                log.error("❌ Upload failed.")
                log.error(f"stdout:\n{e.stdout}")
                log.error(f"stderr:\n{e.stderr}")
                raise

        with log_section("🌐 Generating shareable link..."):
            try:
                result = subprocess.run(
                    [rclone, "link", full_remote_path],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                share_url = result.stdout.strip()

                # Handle Dropbox
                if "dropbox.com" in share_url:
                    # Force raw preview link
                    share_url = share_url.replace(
                        "www.dropbox.com", "dl.dropboxusercontent.com"
                    )
                    share_url = share_url.replace("&dl=0", "")
                    share_url = share_url.replace("&dl=1", "")

                log.info(f"🔗 Shareable URL: {share_url}")
                return share_url
            except subprocess.CalledProcessError as e:
                log.error("❌ Failed to generate shareable link.")
                log.error(f"stdout:\n{e.stdout}")
                log.error(f"stderr:\n{e.stderr}")
                raise
