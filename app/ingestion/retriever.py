from app.ingestion.vector_store import (
    load_embeddings,
    load_index,
    search_index,
)
from app.ingestion.embedder import embed_text


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
    ) -> None:
        self.chunks, _ = load_embeddings(
            embeddings_path
        )

        self.index = load_index(
            index_path
        )

        self.top_k = top_k
        self.similarity_threshold = (
            similarity_threshold
        )

    def retrieve(
        self,
        query: str,
    ) -> list[dict]:
        """Retrieve relevant chunks for a query."""
        query_embedding = embed_text(
            query
        )

        return search_index(
            query_embedding=query_embedding,
            index=self.index,
            chunks=self.chunks,
            top_k=self.top_k,
            similarity_threshold=self.similarity_threshold,
        )
