""" Holds all constants for the project. """
from enum import Enum


class Language(Enum):
    """ Enum for supported languages."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CPP = "cpp"
    C = "c"
    GO = "go"
    RUST = "rust"
    KOTLIN = "kotlin"
    C_SHARP = "c_sharp"
    OBJECTIVE_C = "objective_c"
    SCALA = "scala"
    LUA = "lua"
    HASKELL = "haskell"
    RUBY = "ruby"
    UNKNOWN = "unknown"


class EmbeddingsModel(Enum):
    """ Enum for supported embeddings models."""
    OPENAI_TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"
    OPENAI_TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
