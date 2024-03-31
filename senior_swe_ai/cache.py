""" This module contains functions to create and get the cache directory
for the application.
"""
import json
import os
import platform
from pathlib import Path

from altair import Self


class VectorCache:
    """ 
    VectorCache class for storing vector data 

    Attributes:
    filename: str - The name of the file
    vector_ids: list[str] - The list of vector ids
    commit_hash: str - The commit hash of the file

    """

    def __init__(self, filename, vec_ids, commit_hash) -> None:
        self.filename = filename
        self.vector_ids = vec_ids
        self.commit_hash = commit_hash

    def to_json(self) -> str:
        """Convert the object to json"""
        return {
            "filename": self.filename,
            "commit_hash": self.commit_hash,
            "vector_ids": self.vector_ids,
        }

    @classmethod
    def from_json(cls, data: dict[str, str]) -> Self:
        """
        Create a VectorCache object from json

        Args:
            data: dict[str, str] - The data to create the object

        Returns:
            VectorCache - The created VectorCache object
        """
        return cls(
            filename=data.get("filename"),
            vec_ids=data.get("vector_ids"),
            commit_hash=data.get("commit_hash"),
        )


def get_cache_path() -> str:
    """
    Get the cache directory path for the application.

    Returns:
        str - The cache directory path
    """
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
    """
    Create the cache directory for the application.

    Returns:
        None
    """
    if not os.path.exists(get_cache_path()):
        path = Path(get_cache_path())
        path.mkdir(parents=True, exist_ok=True)


def load_vec_cache(filename: str) -> dict[str, VectorCache]:
    """
    Load the vector cache from the given file.

    Args:
        filename: str - The name of the file

    Returns:
        dict[str, VectorCache] - The vector cache
    """
    with open(get_cache_path() + f'/{filename}', 'r', encoding='utf-8') as f:
        vec = json.load(f)
    vec_cache = {}
    for key, value in vec.items():
        vec_cache[key] = VectorCache.from_json(value)
    return vec_cache


def save_vec_cache(vector_cache, filename) -> None:
    """
    Save the vector cache to the given file.

    Args:
        vector_cache: dict[str, VectorCache] - The vector cache
        filename: str - The name of the file

    Returns:
        None
    """
    with open(
        get_cache_path() + "/" + filename, "w", encoding="utf-8"
    ) as vector_cache_file:
        json.dump(vector_cache, default=VectorCache.to_json,
                  fp=vector_cache_file)
