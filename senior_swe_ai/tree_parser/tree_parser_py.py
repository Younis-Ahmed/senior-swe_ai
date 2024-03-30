""" This module is used to parse the python code using the tree-sitter library. """
from typing import Tuple
import warnings
import tree_sitter
from tree_sitter import Node
from senior_swe_ai.consts import Language
from senior_swe_ai.tree_parser.base import BaseTreeParser, TreeParserMethodNode
from senior_swe_ai.tree_parser.tree_parser_registry import TreeParserRegistry


class TreeParsePy(BaseTreeParser):
    """Class to parse Python code using the tree-sitter library."""

    def __init__(self) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            super().__init__(
                Language.PYTHON, "function_definition", "identifier", "expression_statement"
            )

    def parse(self, file_bytes: bytes) -> list[TreeParserMethodNode]:
        """
        Parse the Python code using the tree-sitter library.

        Args:
            file_bytes (bytes): The Python code in bytes.

        Returns:
            list[TreeParserMethodNode]: A list of method nodes.
        """
        self.tree = self.parser.parse(file_bytes)
        result = []
        methods: list = self._query_all_methods(self.tree.root_node)
        for method in methods:
            method_name: str | None = self._query_method_name(method)
            doc_comment: str | None = self._query_doc_comment(method)
            result.append(TreeParserMethodNode(
                method_name, doc_comment, None, method))
        return result

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
                if child.type == self.method_name_identifier:
                    return child.text.decode()
        return None

    def _query_all_methods(self, node: tree_sitter.Node) -> list:
        """
        Recursively query all methods in the tree-sitter parse tree.

        Args:
            node (tree_sitter.Node): The tree-sitter node.

        Returns:
            list: A list of method nodes.
        """
        methods = []
        for child in node.children:
            if child.type == self.method_declaration_identifier:
                methods.append(child)
            if child.type == "class_definition":
                class_body: Node = child.children[-1]
                for child_node in class_body.children:
                    if child_node.type == self.method_declaration_identifier:
                        methods.append(child_node)
        return methods

    def _query_doc_comment(self, node: tree_sitter.Node) -> str | None:
        """
        Query the documentation comment from the tree-sitter node.

        Args:
            node (tree_sitter.Node): The tree-sitter node.

        Returns:
            str | None: The documentation comment if found, None otherwise.
        """
        query_code = """
            (function_definition
                body: (block . (expression_statement (string)) @function_doc_str))
        """
        doc_str_query: tree_sitter.Query = self.language.query(query_code)
        doc_strs: tree_sitter.List[Tuple[Node, str]
                                   ] = doc_str_query.captures(node)

        if doc_strs:
            return doc_strs[0][0].text.decode()

        return None


TreeParserRegistry.register_treesitter(Language.PYTHON, TreeParsePy)
