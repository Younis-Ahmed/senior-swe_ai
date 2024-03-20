"""
vector store for storing embeddings and their 
metadata, to enable fast search and retrieval
"""
from typing import Any, Dict, List, Optional, Tuple
import os
import inquirer
from langchain.schema import Document
from langchain_community.vectorstores import faiss


class VectorStore:
    """
    VectorStore for storing embeddings and their metadata
    """
    def __init__(self, embed_mdl, name):
        self.embed_mdl = embed_mdl
        self.name = name

    def idx_docs(self, docs: List[Document]) -> None:
        """Index the given documents"""
        pass