"""     Java tree parser module"""
import warnings
from senior_swe_ai.consts import Language
from senior_swe_ai.tree_parser.base import BaseTreeParser
from senior_swe_ai.tree_parser.tree_parser_registry import TreeParserRegistry


class TreeParserJava(BaseTreeParser):
    """Class to parse Java code using the tree-sitter library."""

    def __init__(self) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            super().__init__(
                Language.JAVA, "method_declaration", "identifier", "block_comment"
            )


TreeParserRegistry.register_treesitter(Language.JAVA, TreeParserJava)
