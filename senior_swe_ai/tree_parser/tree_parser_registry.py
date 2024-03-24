"""Registry for tree-sitter parsers."""
from senior_swe_ai.consts import Language


class TreeParserRegistry:
    """Registry for tree-sitter parsers."""
    _registry = {}

    @classmethod
    def register_treesitter(cls, name, treesitter_class) -> None:
        """Register a tree-sitter parser."""
        cls._registry[name] = treesitter_class

    @classmethod
    def create_treesitter(cls, name: Language):
        """Factory method to create a tree-sitter parser for the given language."""
        treesitter_class = cls._registry.get(name)
        if treesitter_class:
            return treesitter_class()

        raise ValueError("Invalid tree type")
