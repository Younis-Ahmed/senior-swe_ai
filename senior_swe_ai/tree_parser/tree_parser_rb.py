""" This module contains the Ruby tree parser. """

import warnings
import tree_sitter
from senior_swe_ai.consts import Language
from senior_swe_ai.tree_parser.base import BaseTreeParser
from senior_swe_ai.tree_parser.tree_parser_registry import TreeParserRegistry


class TreeParseRuby(BaseTreeParser):
    """Class to parse Ruby code using the tree-sitter library."""

    def __init__(self) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            super().__init__(
                Language.RUBY, "method", "identifier", "comment"
            )

    def _query_all_methods(
        self,
        node: tree_sitter.Node,
    ) -> list:
        methods = []
        if node.type == self.method_declaration_identifier:
            doc_comment = []
            doc_comment_node = node
            while (
                doc_comment_node.prev_named_sibling
                and doc_comment_node.prev_named_sibling.type == self.doc_comment_identifier
            ):
                doc_comment_node: tree_sitter.Node = doc_comment_node.prev_named_sibling
                doc_comment.insert(0, doc_comment_node.text.decode())
            methods.append(
                {"method": node, "doc_comment": "\n".join(doc_comment)})
        else:
            for child in node.children:
                methods.extend(self._query_all_methods(child))
        return methods


TreeParserRegistry.register_treesitter(Language.RUBY, TreeParseRuby)
