"""This module contains the TreeParserC class, which is responsible for 
parsing C code using the tree-sitter library."""
import warnings
import tree_sitter
from senior_swe_ai.consts import Language
from senior_swe_ai.tree_parser.base import BaseTreeParser
from senior_swe_ai.tree_parser.tree_parser_registry import TreeParserRegistry


class TreeParserC(BaseTreeParser):
    """
    Class to parse C code using the tree-sitter library.

    Attributes:
        method_declaration_identifier (str): The tree-sitter node type for method declarations.
        method_name_identifier (str): The tree-sitter node type for method names.
        doc_comment_identifier (str): The tree-sitter node type for documentation comments.

    """

    def __init__(self) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            super().__init__(Language.C, "function_definition", "identifier", "comment")

    def _query_method_name(self, node: tree_sitter.Node) -> str | None:
        """
        Query the method name from the tree-sitter node.

        Args:
            node (tree_sitter.Node): The tree-sitter node.

        Returns:
            str | None: The method name if found, None otherwise.

        """
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


TreeParserRegistry.register_treesitter(Language.C, TreeParserC)
