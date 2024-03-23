"""Module for handling file I/O operations"""
import os
from typing import List, Optional, Tuple

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import Language
from senior_swe_ai.git_process import get_hash
from senior_swe_ai.llm_handler import get_langchain_language, get_langchain_text_splitters
from senior_swe_ai.tree_parser.base import Treesitter, TreesitterMethodNode


def get_extension(file_path: str) -> str:
    """Get the file extension from the file path"""
    return '.' + file_path.split('.')[-1]

# TODO (senior_swe_ai): Add type hints, fix none return type
def parse_code_files(code_files: list[str]) -> list[Document]:
    """Parse the given code files and return a list of Documents"""
    documents: list = []
    for code_file in code_files:
        file_bytes, commit_hash, programming_language = read_file_and_get_metadata(
            code_file)
        if programming_language is None:
            continue

        code_splitter: RecursiveCharacterTextSplitter = create_character_text_splitter(
            programming_language)
        treesitter_nodes: List[TreesitterMethodNode] = parse_file_with_treesitter(
            file_bytes, programming_language)

        documents.extend(create_documents_from_nodes(
            treesitter_nodes, code_file, commit_hash, code_splitter, programming_language))

    return documents


def read_file_and_get_metadata(code_file: str) -> Tuple[bytes, str, Optional[Language]]:
    """Read the file and get the metadata"""
    with open(code_file, "r", encoding="utf-8") as file:
        file_bytes: bytes = file.read().encode()
        commit_hash: str = get_hash(code_file)

        file_extension: str = get_extension(code_file)
        programming_language: Language | None = get_langchain_text_splitters(
            file_extension)

    return file_bytes, commit_hash, programming_language


def parse_file_with_treesitter(
        file_bytes: bytes,
        programming_language: Language
) -> list[TreesitterMethodNode]:
    """Parse the file using Treesitter and return the method nodes"""
    treesitter_parser = Treesitter.create_treesitter(programming_language)
    treesitter_nodes: list[TreesitterMethodNode] = treesitter_parser.parse(
        file_bytes)

    return treesitter_nodes


def create_documents_from_nodes(
        treesitter_nodes: list[TreesitterMethodNode],
        code_file: str,
        commit_hash: str,
        code_splitter: RecursiveCharacterTextSplitter,
        programming_language: Language
) -> list[Document]:
    """Create documents from the Treesitter nodes and return them as a list"""
    documents: list = []
    for node in treesitter_nodes:
        method_source_code = node.method_source_code
        filename: str = os.path.basename(code_file)

        if node.doc_comment and programming_language != Language.PYTHON:
            method_source_code = node.doc_comment + "\n" + method_source_code

        splitted_documents = [method_source_code]
        if code_splitter:
            splitted_documents: List[str] = code_splitter.split_text(
                method_source_code)

        for splitted_document in splitted_documents:
            document = Document(
                page_content=splitted_document,
                metadata={
                    "filename": filename,
                    "method_name": node.name,
                    "commit_hash": commit_hash,
                },
            )
            documents.append(document)

    return documents


def create_character_text_splitter(language: Language) -> RecursiveCharacterTextSplitter:
    """Create a RecursiveCharacterTextSplitter for the given language"""
    langchain_language: Language | None = get_langchain_language(language)
    if langchain_language:
        return RecursiveCharacterTextSplitter.from_language(
            language=langchain_language,
            chunk_size=512,
            chunk_overlap=128,
        )
    return RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=128,
    )
