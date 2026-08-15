import json
from dataclasses import asdict
from pathlib import Path

from app.ingestion.models import Chunk


def save_chunks(
    chunks: list[Chunk],
    output_path: str,
) -> None:
    """Save document chunks as a JSON file.

    Args:
        chunks: Chunks to save.
        output_path: Destination path for the JSON file.
    """
    path = Path(output_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = [
        asdict(chunk)
        for chunk in chunks
    ]

    path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
