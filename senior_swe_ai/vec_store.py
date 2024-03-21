"""
vector store for storing embeddings and their 
metadata, to enable fast search and retrieval
"""
from typing import Any, Dict, List, Optional, Tuple
import os
import inquirer
from langchain.schema import Document
from langchain_community.vectorstores.faiss import FAISS as faiss
from langchain_core.vectorstores import VectorStoreRetriever

from senior_swe_ai.cache import VectorCache, get_cache_path


class VectorStore:
    """
    VectorStore for storing embeddings and their metadata
    """

    def __init__(self, embed_mdl, name):
        self.embed_mdl = embed_mdl
        self.name = name
        self.vec_cache = {}
        self.db = {}
        self.retrieval = {}

    def _create_vec_cache(self, docs: List[Document]):
        """Create a cache for the vectors"""
        idx_docstore: Dict[int, str] = self.db.index_to_docstore_id
        for idx, doc in enumerate(docs):
            find_doc: str | Document = self.db.docstore.search(
                idx_docstore[idx])
            if find_doc:
                if self.vec_cache.get(find_doc.metadata["filename"]):
                    self.vec_cache[find_doc.metadata["filename"]
                                   ].vector_ids.append(idx_docstore[idx])
                else:
                    self.vec_cache[find_doc.metadata["filename"]] = VectorCache(
                        doc.metadata["filename"], [
                            idx_docstore[idx]], doc.metadata["commit_hash"]
                    )

    def idx_docs(self, docs: List[Document]) -> None:
        """Index the given documents"""
        self.db: faiss = faiss.from_documents(docs, self.embed_mdl)
        idx: bytes = self.db.serialize_to_bytes()
        with open(get_cache_path() + f'/{self.name}.faiss', 'wb') as f:
            f.write(idx)

        self._create_vec_cache(docs)

        self.retrieval: VectorStoreRetriever = self.db.as_retriever(
            search_type="mmr", search_kwargs={"k": 8})

    def similarity_search(self, query: str) -> List[Document]:
        """Search for similar documents to the given query"""
        return self.db.similarity_search(query, k=4)