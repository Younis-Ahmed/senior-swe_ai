"""This module contains functions to interact with LLMs and their embeddings
    using Langchain
"""
from langchain_text_splitters import Language


def get_langchain_text_splitters(language: Language) -> Language | None:
    """Get the Langchain text splitters for the given language"""

    lang_map: dict[str, Language] = {
        ".py": Language.PYTHON,
        ".js": Language.JS,
        ".jsx": Language.JS,
        ".mjs": Language.JS,
        ".cjs": Language.JS,
        ".ts": Language.TS,
        ".tsx": Language.TS,
        ".java": Language.JAVA,
        ".kt": Language.KOTLIN,
        ".rs": Language.RUST,
        ".go": Language.GO,
        ".cpp": Language.CPP,
        ".c": Language.C,
        ".cs": Language.CSHARP,
        ".rb": Language.RUBY,
    }
    return lang_map.get(language)
