"""     This module contains functions to interact with git repositories. """
import os
import subprocess
from senior_swe_ai.consts import EXCLUDE_DIRS, EXCLUDE_FILES, INCLUDE_FILES


def is_git_repo() -> bool:
    """ Check if the current directory is a git repository """
    if not subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"], capture_output=True, check=True
    ).stdout:
        return False
    return True


def get_repo_root() -> str:
    """ Get the root directory of the git repository """
    return subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, check=True, text=True
    ).stdout.strip()


def get_repo_name() -> str:
    """ Get the name of the git repository """
    return subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, check=True, text=True
    ).stdout.strip().split('/')[-1]


def recursive_load_files() -> list[str]:
    """ Load all files in the git repository """
    git_root: str = get_repo_root()
    file_list: list = []

    for root, _, files in os.walk(git_root):
        if any(blacklist in root for blacklist in EXCLUDE_DIRS):
            continue
        for file in files:
            file_ext: str = os.path.splitext(file)[1]
            if any(whitelist == file_ext for whitelist in INCLUDE_FILES):
                if file not in EXCLUDE_FILES:
                    file_list.append(os.path.join(root, file))

    return file_list
