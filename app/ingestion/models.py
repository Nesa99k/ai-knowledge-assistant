from dataclasses import dataclass


@dataclass
class Chunk:
    """Represents a semantically meaningful chunk of a source document."""

    text: str
    source: str
    section: str
    chunk_id: int
    pdf_page_number: int
    book_page_number: int | None
