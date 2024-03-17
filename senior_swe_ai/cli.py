""" SeniorSWE cli tool utilize AI to help you with your project """
from argparse import ArgumentParser, Namespace
import os
import sys
from langchain_openai import OpenAIEmbeddings
from senior_swe_ai.git_process import (
    is_git_repo, get_repo_name, get_repo_root, recursive_load_files
)
from senior_swe_ai.conf import config_init, load_conf, append_conf
from senior_swe_ai.cache import create_cache_dir, get_cache_path


def main() -> None:
    """ __main__ """
    parser = ArgumentParser(
        description='SeniorSWE cli tool utilize AI to help you with your project'
    )

    parser.add_argument(
        'options', choices=['init', 'chat'],
        help="'init': initialize the app. 'chat': chat with the AI"
    )

    args: Namespace = parser.parse_args()

    if args.options == 'init':
        print('Initializing the app...')
        config_init()
        sys.exit()

    if not is_git_repo():
        print('The current directory is not a git repository')
        sys.exit(1)

    repo_name: str = get_repo_name()
    repo_root: str = get_repo_root()

    append_conf({'repo_name': repo_name, 'repo_root': repo_root})

    try:
        conf: dict[str, str] = load_conf()
    except FileNotFoundError:
        config_init()
        append_conf({'repo_name': repo_name, 'repo_root': repo_root})
        conf = load_conf()

    create_cache_dir()

    embed_mdl = OpenAIEmbeddings(
        model=conf['embed_model'], api_key=conf['api_key'])

    if not os.path.exists(get_cache_path() + f'/{repo_name}.faiss'):
        # all files in the git repository
        files: list[str] = recursive_load_files()
        


if __name__ == '__main__':
    main()
