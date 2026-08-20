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
    section: str | None = None,
) -> list[dict]:
    """Search FAISS with optional metadata filtering."""

    query = np.array(
        [query_embedding],
        dtype="float32",
    )

    # Retrieve more candidates when metadata filtering is used.
    search_k = top_k

    if section is not None:
        search_k = min(
            len(chunks),
            max(top_k * 5, 20),
        )

    scores, indices = index.search(
        query,
        search_k,
    )

    results = []

    for score, index_id in zip(
        scores[0],
        indices[0],
    ):
        if index_id < 0:
            continue

        if score < similarity_threshold:
            continue

        chunk = chunks[index_id]

        if section is not None:
            if chunk["section"] != section:
                continue

        results.append(
            {
                "similarity": float(score),
                "chunk": chunk,
            }
        )

        if len(results) >= top_k:
            break

    return results
