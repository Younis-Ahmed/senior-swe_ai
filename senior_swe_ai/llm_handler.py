"""This module contains functions to interact with LLMs and their embeddings
    using Langchain
"""
from langchain import text_splitter
from senior_swe_ai.consts import Language


def get_langchain_text_splitters(language: Language) -> Language | None:
    """Get the Langchain text splitters for the given language"""

    lang_map: dict[str, Language] = {
        ".py": Language.PYTHON,
        ".js": Language.JAVASCRIPT,
        ".jsx": Language.JAVASCRIPT,
        ".mjs": Language.JAVASCRIPT,
        ".cjs": Language.JAVASCRIPT,
        ".ts": Language.TYPESCRIPT,
        ".tsx": Language.TYPESCRIPT,
        ".java": Language.JAVA,
        ".kt": Language.KOTLIN,
        ".rs": Language.RUST,
        ".go": Language.GO,
        ".cpp": Language.CPP,
        ".c": Language.C,
        ".cs": Language.C_SHARP,
        ".hs": Language.HASKELL,
        ".rb": Language.RUBY,
    }
    return lang_map.get(language, None)


def get_langchain_language(language: Language) -> text_splitter.Language | None:
    """Get the Langchain language for the given language"""
    lang_map: dict[Language, text_splitter.Language] = {
        Language.PYTHON: text_splitter.Language.PYTHON,
        Language.JAVASCRIPT: text_splitter.Language.JS,
        Language.TYPESCRIPT: text_splitter.Language.TS,
        Language.JAVA: text_splitter.Language.JAVA,
        Language.KOTLIN: text_splitter.Language.KOTLIN,
        Language.RUST: text_splitter.Language.RUST,
        Language.GO: text_splitter.Language.GO,
        Language.CPP: text_splitter.Language.CPP,
        Language.C_SHARP: text_splitter.Language.CSHARP,
        Language.RUBY: text_splitter.Language.RUBY,
        Language.HASKELL: None,  # : Add Haskell support
    }
    return lang_map.get(language, None)
