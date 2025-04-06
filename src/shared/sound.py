import contextlib
import os
from pathlib import Path

# Suppress stdout and stderr while importing and initializing pygame
with open(os.devnull, "w") as devnull, contextlib.redirect_stdout(
    devnull
), contextlib.redirect_stderr(devnull):
    import pygame

    pygame.mixer.init()

from src.shared.structured_logger import log


def play_sound(path: Path, volume: float = 0.5) -> None:
    try:
        pygame.mixer.music.load(str(path))
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
    except Exception as e:
        log.warning(f"⚠️ Failed to play sound: {path} - {e}")
