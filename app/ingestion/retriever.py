from app.ingestion.embedder import embed_text
from app.ingestion.vector_store import (
    load_embeddings,
    load_index,
    search_index,
)
import numpy as np
import faiss


EMBEDDINGS_PATH = (
    "data/processed/disabilities_embeddings.json"
)

INDEX_PATH = (
    "data/processed/disabilities.index"
)


class Retriever:
    """Retrieve relevant chunks using vector similarity."""

    def __init__(
        self,
        embeddings_path: str = EMBEDDINGS_PATH,
        index_path: str = INDEX_PATH,
        top_k: int = 5,
        similarity_threshold: float = 0.75,
        section_similarity_threshold: float = 0.60,
        table_similarity_threshold: float = 0.60,
    ) -> None:

        self.chunks, self.embeddings = load_embeddings(
            embeddings_path
        )

        self.index = load_index(
            index_path
        )

        self.top_k = top_k
        self.similarity_threshold = (
            similarity_threshold
        )
        self.section_similarity_threshold = (
            section_similarity_threshold
        )
        self.table_similarity_threshold = (
            table_similarity_threshold
        )

    def _filter_chunks(
        self,
        section: str | None = None,
        include_table: bool = False,
    ) -> list[int]:
        """Return indices of chunks matching metadata filters."""

        matching_indices = []

        for index, chunk in enumerate(self.chunks):

            if section is not None:
                if chunk["section"] != section:
                    if not (
                        include_table and
                        chunk["section"]
                        == "Table 1 - Frequently occurring disabilities"
                    ):
                        continue

            matching_indices.append(index)

        return matching_indices

    def retrieve(
        self,
        query: str,
        section: str | None = None,
    ) -> list[dict]:
        """Retrieve relevant chunks with optional metadata filtering."""

        query_embedding = embed_text(
            query
        )

        if section is None:
            is_table_query = (
                "table 1" in query.lower()
                or "table one" in query.lower()
                or "according to table" in query.lower()
            )
            threshold = (
                self.table_similarity_threshold
                if is_table_query
                else self.similarity_threshold
            )
            return search_index(
                query_embedding=query_embedding,
                index=self.index,
                chunks=self.chunks,
                top_k=self.top_k,
                similarity_threshold=threshold,
            )
        is_table_query = (
            "table 1" in query.lower()
            or "table one" in query.lower()
            or "according to table" in query.lower()
        )

        matching_indices = self._filter_chunks(
            section=section,
            include_table=is_table_query,
        )

        if not matching_indices:
            return []

        filtered_embeddings = self.embeddings[
            matching_indices
        ]

        filtered_index = faiss.IndexFlatIP(
            filtered_embeddings.shape[1]
        )

        filtered_index.add(
            filtered_embeddings
        )

        filtered_chunks = [
            self.chunks[index]
            for index in matching_indices
        ]
        threshold = (
            self.table_similarity_threshold
            if is_table_query
            else self.section_similarity_threshold
        )

        return search_index(
            query_embedding=query_embedding,
            index=filtered_index,
            chunks=filtered_chunks,
            top_k=self.top_k,
            similarity_threshold=threshold,
        )
