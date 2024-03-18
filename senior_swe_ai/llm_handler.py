"""This module contains functions to interact with LLMs and their embeddings
    using Langchain
"""
from langchain_text_splitters import Language


def get_langchain_text_splitters(language: Language):
    """Get the Langchain text splitters for the given language"""

    if language == Language.PYTHON:
        return Language.PYTHON
    elif language == Language.JS:
        return Language.JS
    elif language == Language.TS:
        return Language.TS
    elif language == Language.JAVA:
        return Language.JAVA
    elif language == Language.KOTLIN:
        return Language.KOTLIN
    elif language == Language.RUST:
        return Language.RUST
    elif language == Language.GO:
        return Language.GO
    elif language == Language.CPP:
        return Language.CPP
    elif language == Language.CSHARP:
        return Language.CSHARP
    elif language == Language.RUBY:
        return Language.RUBY
    else:
        return None
