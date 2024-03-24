""" This module is responsible for parsing the code using the tree-sitter library. """
import warnings
from senior_swe_ai.consts import Language
from senior_swe_ai.tree_parser.base import BaseTreeParser
from senior_swe_ai.tree_parser.tree_parser_registry import TreeParserRegistry


class TreeParseTypescript(BaseTreeParser):
    """Class to parse TypeScript code using the tree-sitter library."""

    def __init__(self) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            super().__init__(
                Language.TYPESCRIPT, "function_declaration", "identifier", "comment"
            )


TreeParserRegistry.register_treesitter(
    Language.TYPESCRIPT, TreeParseTypescript)
