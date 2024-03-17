""" This module contains functions to create and get the cache directory
for the application.
"""
import os
import platform
from pathlib import Path


def get_cache_path() -> str:
    """Get the cache directory path for the application."""
    system: str = platform.system()

    if system in ('Linux', 'Darwin'):
        user_home: str = os.path.expanduser("~")
        cache_dir: str = os.path.join(user_home, ".cache", "senior_swe_ai")
    elif system == "Windows":
        user_home = os.path.expanduser("~")
        cache_dir = os.path.join(user_home, "AppData",
                                 "Local", "senior_swe_ai")
    else:
        raise NotImplementedError(f"Unsupported platform: {system}")

    return cache_dir


def create_cache_dir() -> None:
    """Create the cache directory for the application."""
    if not os.path.exists(get_cache_path()):
        path = Path(get_cache_path())
        path.mkdir(parents=True, exist_ok=True)
