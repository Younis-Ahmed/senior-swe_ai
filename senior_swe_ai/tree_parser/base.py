"""Base class for tree-sitter parsers."""
from abc import ABC
from typing import Any

import tree_sitter
from tree_sitter_languages import get_language, get_parser

from senior_swe_ai.consts import Language
from senior_swe_ai.tree_parser.tree_parser_registry import TreesitterRegistry


class TreesitterMethodNode:  # pylint: disable=too-few-public-methods
    """Class to represent a method node in the tree-sitter parse tree."""

    def __init__(
        self,
        name: "str | bytes | None",
        doc_comment: "str | None",
        method_source_code: "str | None",
        node: tree_sitter.Node,
    ) -> None:
        self.name: str | bytes | None = name
        self.doc_comment: str | None = doc_comment
        self.method_source_code: str = method_source_code or node.text.decode()
        self.node: tree_sitter.Node = node


class Treesitter(ABC):
    """ Base class for tree-sitter parsers."""

    def __init__(
        self,
        language: Language,
        method_declaration_identifier: str,
        name_identifier: str,
        doc_comment_identifier: str,
    ) -> None:
        self.parser: tree_sitter.Parser = get_parser(language.value)
        self.language: tree_sitter.Language = get_language(language.value)
        self.method_declaration_identifier: str = method_declaration_identifier
        self.method_name_identifier: str = name_identifier
        self.doc_comment_identifier: str = doc_comment_identifier
        self.tree: tree_sitter.Tree | None = None

    @staticmethod
    def create_treesitter(lang: Language) -> Any:
        """Factory method to create a tree-sitter parser for the given language."""
        return TreesitterRegistry.create_treesitter(lang)

    def parse(self, file_bytes: bytes) -> list[TreesitterMethodNode]:
        """Parse the given file and return a list of method nodes."""
        self.tree = self.parser.parse(file_bytes)
        result = []
        methods = self._query_all_methods(self.tree.root_node)
        for method in methods:
            method_name: str | None = self._query_method_name(method["method"])
            doc_comment = method["doc_comment"]
            result.append(
                TreesitterMethodNode(
                    method_name, doc_comment, None, method["method"])
            )
        return result

    def _query_all_methods(
        self,
        node: tree_sitter.Node,
    ) -> list:
        methods = []
        if node.type == self.method_declaration_identifier:
            doc_comment_node = None
            if (
                node.prev_named_sibling
                and node.prev_named_sibling.type == self.doc_comment_identifier
            ):
                doc_comment_node: str = node.prev_named_sibling.text.decode()
            methods.append({"method": node, "doc_comment": doc_comment_node})
        else:
            for child in node.children:
                methods.extend(self._query_all_methods(child))
        return methods

    def _query_method_name(self, node: tree_sitter.Node) -> str | None:
        if node.type == self.method_declaration_identifier:
            for child in node.children:
                if child.type == self.method_name_identifier:
                    return child.text.decode()
        return None
