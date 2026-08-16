import json
from pathlib import Path

from app.ingestion.embedder import embed_text


def embed_chunks(
    input_path: str,
    output_path: str,
) -> None:
    """Create embeddings for all chunks in a JSON file.
    Args: 
    input_path: Path to the chunk JSON file.
    output_path: Path where the embedded chunks are saved. 
    """
    input_file = Path(input_path)
    output_file = Path(output_path)

    with input_file.open("r", encoding="utf-8",) as file:
        chunks = json.load(file)

    for chunk in chunks:
        chunk["embedding"] = embed_text(chunk["text"])

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    with output_file.open("w", encoding="utf-8") as file:
        json.dump(
            chunks,
            file,
            ensure_ascii=False,
            indent=2
        )
