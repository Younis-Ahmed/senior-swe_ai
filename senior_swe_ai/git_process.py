"""     This module contains functions to interact with git repositories. """
import subprocess


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
