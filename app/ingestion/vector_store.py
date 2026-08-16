import numpy as np
import faiss
from pathlib import Path
import json


def load_embeddings(
    file_path: str,
) -> tuple[list[dict], np.ndarray]:
    """Load chunks and their embeddings from JSON."""
    path = Path(file_path)

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        chunks = json.load(file)

    embeddings = np.array(
        [chunk["embedding"] for chunk in chunks],
        dtype="float32",
    )

    return chunks, embeddings


def build_index(
    embeddings: np.ndarray,
) -> faiss.Index:
    """Build a FAISS index for cosine similarity."""
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    return index


def save_index(
    index: faiss.Index,
    file_path: str,
) -> None:
    """Save a FAISS index to disk."""
    path = Path(file_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    faiss.write_index(
        index,
        str(path),
    )


def load_index(
    file_path: str,
) -> faiss.Index:
    """Load a FAISS index from disk."""
    return faiss.read_index(
        str(file_path)
    )


def search_index(
    query_embedding: list[float],
    index: faiss.Index,
    chunks: list[dict],
    top_k: int = 5,
    similarity_threshold: float = 0.75,
) -> list[dict]:
    """Search the FAISS index using top-k and similarity threshold."""
    query = np.array(
        [query_embedding],
        dtype="float32",
    )

    scores, indices = index.search(
        query,
        top_k,
    )

    results = []

    for score, index_id in zip(
        scores[0],
        indices[0],
    ):
        if score < similarity_threshold:
            continue

        results.append(
            {
                "similarity": float(score),
                "chunk": chunks[index_id],
            }
        )

    return results
