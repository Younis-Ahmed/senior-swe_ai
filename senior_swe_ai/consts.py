""" Holds all constants for the project. """
from enum import Enum
from importlib.metadata import distribution, PackageNotFoundError


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


class FaissModel(Enum):
    """ Enum for supported faiss models."""
    FAISS_CPU = "faiss-cpu"
    FAISS_GPU = "faiss-gpu"


EXCLUDE_DIRS: list[str] = [
    "__pycache__",
    ".pytest_cache",
    ".venv",
    ".git",
    ".idea",
    "venv",
    "env",
    "node_modules",
    "dist",
    "build",
    ".vscode",
    ".github",
    ".gitlab",
    ".angular",
    "cdk.out",
    ".aws-sam",
    ".terraform",
    ".mypy_cache",
    ".hypothesis",
    ".junit",
    ".metals",
    ".bloop",
    ".sbt",
    ".dotty",
    ".gradle",
    ".mvn",
    ".ccls-cache",
    ".cmake",
    ".stack-work",
    ".cabal-sandbox",
    ".cargo",
    ".gogradle",
    ".gocache",
]

EXCLUDE_FILES: list[str] = [
    "package-lock.json",
    "package.json",
    "__init__.py",
    ".gitignore",
    ".gitattributes",
    "yarn.lock",
    "requirements.txt",
    "setup.py",
    "Dockerfile",
    "docker-compose.yml",
    "Makefile",
    "README.md",
    "LICENSE",
    ".travis.yml",
    ".babelrc",
    ".eslintrc.js",
    ".prettierrc",
    "tsconfig.json",
    "webpack.config.js",
    "pom.xml",
    "build.gradle",
    "Cargo.toml",
    "Cargo.lock",
    "go.mod",
    "go.sum",
    "Gemfile",
    "Gemfile.lock",
    "Rakefile",
    "composer.json",
    "composer.lock",
]

INCLUDE_FILES: list[str] = [
    ".js",
    ".mjs",
    ".ts",
    ".tsx",
    ".css",
    ".scss",
    ".less",
    ".html",
    ".htm",
    ".json",
    ".py",
    ".java",
    ".c",
    ".cpp",
    ".cs",
    ".go",
    ".php",
    ".rb",
    ".rs",
    ".swift",
    ".kt",
    ".scala",
    ".m",
    ".h",
    ".sh",
    ".pl",
    ".pm",
    ".lua",
    ".sql",
    ".yaml",
    ".yml",
    ".rst",
    ".md",
    ".hs",
    ".rb",
]


def faiss_installed() -> bool:
    """Check if faiss is installed."""
    for pack in FaissModel:
        try:
            distribution(pack.value)
            return True
        except PackageNotFoundError:
            continue
    return False
