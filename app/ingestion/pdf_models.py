from dataclasses import dataclass
from typing import Literal


ElementType = Literal[
    "text",
    "heading",
    "box",
    "table",
]


@dataclass
class DocumentElement:
    """Represents one ordered element extracted from a PDF page."""

    text: str
    element_type: ElementType = "text"


@dataclass
class DocumentPage:
    """Represents a PDF page with ordered document elements."""

    elements: list[DocumentElement]
    pdf_page_number: int
    book_page_number: int | None
