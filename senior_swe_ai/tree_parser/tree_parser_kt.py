""" This module contains the BaseTreeParser for JavaScript. """
import warnings
from senior_swe_ai.consts import Language
from senior_swe_ai.tree_parser.base import BaseTreeParser
from senior_swe_ai.tree_parser.tree_parser_registry import TreeParserRegistry


class TreeParserKotlin(BaseTreeParser):
    """Class to parse Kotlin code using the tree-sitter library."""

    def __init__(self) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            super().__init__(
                Language.KOTLIN, "function_declaration", "simple_identifier", "comment"
            )


TreeParserRegistry.register_treesitter(Language.KOTLIN, TreeParserKotlin)
