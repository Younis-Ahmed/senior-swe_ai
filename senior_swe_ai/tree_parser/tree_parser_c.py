"""This module contains the TreesitterC class, which is responsible for 
parsing C code using the tree-sitter library."""
import tree_sitter
from senior_swe_ai.consts import Language
from senior_swe_ai.tree_parser.base import Treesitter
from senior_swe_ai.tree_parser.tree_parser_registry import TreesitterRegistry


class TreesitterC(Treesitter):
    """Class to parse C code using the tree-sitter library."""

    def __init__(self):
        super().__init__(Language.C, "function_definition", "identifier", "comment")

    def _query_method_name(self, node: tree_sitter.Node):
        if node.type == self.method_declaration_identifier:
            for child in node.children:
                # if method returns pointer, skip pointer declarator
                if child.type == "pointer_declarator":
                    child = child.children[1]
                if child.type == "function_declarator":
                    for child in child.children:
                        if child.type == self.method_name_identifier:
                            return child.text.decode()
        return None


TreesitterRegistry.register_treesitter(Language.C, TreesitterC)
