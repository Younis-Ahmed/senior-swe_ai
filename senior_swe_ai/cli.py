""" SeniorSWE cli tool utilize AI to help you with your project """
from argparse import ArgumentParser, Namespace
import os
import sys
from typing import List
from langchain.memory import ConversationSummaryMemory
from langchain.chains.conversational_retrieval.base import (
    BaseConversationalRetrievalChain, ConversationalRetrievalChain
)
import pkg_resources
import inquirer
from langchain_core.documents.base import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from senior_swe_ai.file_handler import parse_code_files
from senior_swe_ai.git_process import (
    is_git_repo, get_repo_name, get_repo_root, recursive_load_files
)
from senior_swe_ai.conf import config_init, load_conf, append_conf
from senior_swe_ai.cache import create_cache_dir, get_cache_path, save_vec_cache
from senior_swe_ai.vec_store import VectorStore
from senior_swe_ai.consts import FaissModel


def main() -> None:
    """ __main__ """
    py_version: tuple[int, int] = sys.version_info[:2]
    if py_version < (3, 9) or py_version > (3, 12):
        print('This app requires Python ^3.9.x or >3.12.x')
        sys.exit(1)

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

    vec_store = VectorStore(embed_mdl, repo_name)

    if not os.path.exists(get_cache_path() + f'/{repo_name}.faiss'):
        try:
            pkg_resources.get_distribution('faiss')
        except pkg_resources.DistributionNotFound:
            question = [
                inquirer.List(
                    'install',
                    message='FAISS is not installed. Do you want to install it?',
                    choices=['Yes', 'No'],
                    default='Yes'
                )
            ]
            answer: dict[str, str] = inquirer.prompt(question)
            if answer['install'] == 'Yes':
                question = [
                    inquirer.List(
                        "faiss-installation",
                        message="Please select the appropriate option to install FAISS. \
                            Use gpu if your system supports CUDA",
                        choices=[
                            FaissModel.FAISS_CPU.value,
                            FaissModel.FAISS_GPU.value,
                        ],
                        default=FaissModel.FAISS_CPU.value,
                    )
                ]
                answer: dict[str, str] = inquirer.prompt(question)
                if answer['faiss-installation'] == 'faiss-cpu':
                    os.system('pip install faiss-cpu')
                else:
                    os.system('pip install faiss-gpu')
            else:
                print('FAISS is required for this app to work')
                sys.exit(1)
        # all desired files in the git repository tree
        files: list[str] = recursive_load_files()
        docs: List[Document] = parse_code_files(files)
        vec_store.idx_docs(docs)
        save_vec_cache(vec_store.vec_cache, f'{repo_name}.json')

    vec_store.load_docs()
    chat_mdl = ChatOpenAI(model=conf['chat_model'], api_key=conf['api_key'], temperature=0.9,
                          max_tokens=2048)
    mem = ConversationSummaryMemory(
        llm=chat_mdl, memory_key='chat_history', return_messages=True
    )
    qa: BaseConversationalRetrievalChain = ConversationalRetrievalChain.from_llm(
        chat_mdl, retriever=vec_store.retrieval, memory=mem)

    try:
        continue_chat = True
        while continue_chat:
            question: str = input(conf['username'] + ': ')
            answer = qa(question)
            print(repo_name + ': ' + answer['answer'])

            choice: str = (
                input(
                    '[C]ontinue chatting, [R]eset chat history, or [Q]uit? '
                ).strip().upper()
            )
            if choice == 'C':
                continue
            if choice == 'R':
                mem.clear()
                continue
            if choice == 'Q':
                continue_chat = False
    except KeyboardInterrupt:
        print('\n✌')


if __name__ == '__main__':
    main()
