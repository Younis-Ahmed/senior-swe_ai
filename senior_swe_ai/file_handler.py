"""Module for handling file I/O operations"""


def get_extension(file_path: str) -> str:
    """Get the file extension from the file path"""
    return file_path.split('.')[-1]
