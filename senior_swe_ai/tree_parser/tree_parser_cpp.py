"""Module to parse C++ code using the tree-sitter library."""
import warnings
import tree_sitter
from senior_swe_ai.consts import Language
from senior_swe_ai.tree_parser.base import BaseTreeParser
from senior_swe_ai.tree_parser.tree_parser_registry import TreeParserRegistry


class TreeParserCpp(BaseTreeParser):
    """Class to parse C++ code using the tree-sitter library."""

    def __init__(self) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            super().__init__(Language.CPP, "function_definition", "identifier", "comment")

    def _query_method_name(self, node: tree_sitter.Node) -> str | None:
        if node.type == self.method_declaration_identifier:
            for child in node.children:
                # if method returns pointer, skip pointer declarator
                if child.type == "pointer_declarator":
                    child: tree_sitter.Node = child.children[1]
                if child.type == "function_declarator":
                    for child in child.children:
                        if child.type == self.method_name_identifier:
                            return child.text.decode()
        return None


TreeParserRegistry.register_treesitter(Language.CPP, TreeParserCpp)
