from pathlib import Path
import re

from docling.document_converter import (
    DocumentConverter,
)

from app.ingestion.pdf_models import (
    DocumentElement,
    DocumentPage,
)


HEADER_TEXT = (
    "Handbook for Children with Special Food "
    "and Nutrition Needs"
)

FOOTER_TEXT = (
    "National Food Service Management Institute"
)


def clean_text(text: str) -> str:
    """Clean extracted document text."""

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    cleaned_lines = []

    for line in lines:
        if line == HEADER_TEXT:
            continue

        if FOOTER_TEXT in line:
            continue

        if re.fullmatch(r"\d+", line):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()


def get_book_page_number(
    pdf_page_number: int,
) -> int | None:
    """Map PDF page number to printed page number."""

    if pdf_page_number < 3:
        return None

    return pdf_page_number + 12


def classify_element(
    element,
) -> str:
    """Map a Docling element to our document element type."""

    element_name = type(element).__name__.lower()

    if "table" in element_name:
        return "table"

    if "title" in element_name:
        return "heading"

    if "heading" in element_name:
        return "heading"

    return "text"


def get_element_text(
    element,
) -> str:
    """Extract displayable text from a Docling element."""

    element_type = classify_element(
        element
    )

    if element_type == "table":
        return element.export_to_markdown()

    return getattr(
        element,
        "text",
        "",
    )


def extract_page_elements(
    docling_document,
    pdf_page_number: int,
) -> list[DocumentElement]:
    """Extract ordered elements from one PDF page."""

    elements = []

    for element, _level in docling_document.iterate_items(
        with_groups=True
    ):
        provenance = getattr(
            element,
            "prov",
            None,
        )

        if provenance:
            belongs_to_page = any(
                getattr(
                    item,
                    "page_no",
                    None,
                )
                == pdf_page_number
                for item in provenance
            )

            if not belongs_to_page:
                continue

        element_type = classify_element(
            element
        )

        text = get_element_text(
            element
        )

        text = clean_text(
            text
        )

        if not text:
            continue

        elements.append(
            DocumentElement(
                text=text,
                element_type=element_type,
            )
        )

    return elements


def load_pdf(
    file_path: str,
) -> list[DocumentPage]:
    """Load a PDF using Docling and preserve document structure."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    if path.suffix.lower() != ".pdf":
        raise ValueError(
            f"Expected a PDF file, got: {path.suffix}"
        )

    converter = DocumentConverter()

    result = converter.convert(
        str(path)
    )

    document = result.document

    pages_by_number: dict[
        int,
        list[DocumentElement],
    ] = {}

    for page_no in range(
        1,
        len(document.pages) + 1,
    ):
        pages_by_number[page_no] = (
            extract_page_elements(
                document,
                page_no,
            )
        )

    pages = []

    for pdf_page_number in sorted(
        pages_by_number
    ):
        elements = pages_by_number[
            pdf_page_number
        ]

        if not elements:
            continue

        pages.append(
            DocumentPage(
                elements=elements,
                pdf_page_number=pdf_page_number,
                book_page_number=get_book_page_number(
                    pdf_page_number
                ),
            )
        )

    return pages
