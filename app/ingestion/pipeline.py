from app.ingestion.loader import load_pdf
from app.ingestion.chunker import chunk_pdf_page


INITIAL_SECTION = "Chapter Introduction"


def ingest_pdf(
    file_path: str,
    chunk_size: int = 300,
    overlap: int = 40,
) -> list:
    """Load a PDF and convert it into ordered semantic chunks."""

    pages = load_pdf(file_path)

    chunks = []
    current_section = INITIAL_SECTION
    next_chunk_id = 0

    for page in pages:

        page_chunks, current_section, next_chunk_id = (
            chunk_pdf_page(
                page=page,
                source=file_path,
                section=current_section,
                chunk_size=chunk_size,
                overlap=overlap,
                start_chunk_id=next_chunk_id,
            )
        )

        chunks.extend(page_chunks)

    return chunks
