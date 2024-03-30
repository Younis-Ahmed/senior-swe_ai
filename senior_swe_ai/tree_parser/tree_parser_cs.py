"""This module contains the TreeParserCsharp class, which is responsible 
for parsing C# code using the tree-sitter library."""
from typing import Literal
import warnings
import tree_sitter
from senior_swe_ai.consts import Language
from senior_swe_ai.tree_parser.base import BaseTreeParser
from senior_swe_ai.tree_parser.tree_parser_registry import TreeParserRegistry


class TreeParserCsharp(BaseTreeParser):
    """Class to parse C# code using the tree-sitter library."""

    def __init__(self) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            super().__init__(
                Language.C_SHARP, "method_declaration", "identifier", "comment"
            )

    def _query_method_name(self, node: tree_sitter.Node) -> str | None:
        """
        Query the method name from the tree-sitter node.

        Args:
            node (tree_sitter.Node): The tree-sitter node.

        Returns:
            str | None: The method name if found, None otherwise.

        """
        first_match = None
        if node.type == self.method_declaration_identifier:
            for child in node.children:
                if child.type == self.method_name_identifier and not first_match:
                    first_match: str = child.text.decode()
                elif child.type == self.method_name_identifier and first_match:
                    return child.text.decode()
        return first_match

    def _query_all_methods(self, node: tree_sitter.Node) -> list:
        """
        Recursively query all methods in the tree-sitter parse tree.

        Args:
            node (tree_sitter.Node): The tree-sitter node.

        Returns:
            list: A list of method nodes.


        """
        methods = []
        if node.type == self.method_declaration_identifier:
            doc_comment_nodes = []
            if (
                node.prev_named_sibling
                and node.prev_named_sibling.type == self.doc_comment_identifier
            ):
                current_doc_comment_node: tree_sitter.Node = node.prev_named_sibling
                while (
                    current_doc_comment_node
                    and current_doc_comment_node.type == self.doc_comment_identifier
                ):
                    doc_comment_nodes.append(
                        current_doc_comment_node.text.decode())
                    if current_doc_comment_node.prev_named_sibling:
                        current_doc_comment_node = (
                            current_doc_comment_node.prev_named_sibling
                        )
                    else:
                        current_doc_comment_node = None

            doc_comment_str: Literal[''] = ""
            doc_comment_nodes.reverse()
            for doc_comment_node in doc_comment_nodes:
                doc_comment_str += doc_comment_node + "\n"
            if doc_comment_str.strip() != "":
                methods.append(
                    {"method": node, "doc_comment": doc_comment_str.strip()})
            else:
                methods.append({"method": node, "doc_comment": None})
        else:
            for child in node.children:
                methods.extend(self._query_all_methods(child))
        return methods


TreeParserRegistry.register_treesitter(Language.C_SHARP, TreeParserCsharp)
