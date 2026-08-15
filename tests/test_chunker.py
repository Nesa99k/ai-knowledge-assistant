from app.ingestion.chunker import (
    chunk_pdf_page,
    count_tokens,
)
from app.ingestion.pdf_models import (
    DocumentElement,
    DocumentPage,
)


def make_page(
    text: str,
    pdf_page_number: int = 4,
    book_page_number: int = 16,
) -> DocumentPage:
    elements = [
        DocumentElement(
            text=part.strip(),
            element_type="text",
        )
        for part in text.split("\n\n")
        if part.strip()
    ]

    return DocumentPage(
        elements=elements,
        pdf_page_number=pdf_page_number,
        book_page_number=book_page_number,
    )


def test_chunk_pdf_page_preserves_page_metadata():
    page = make_page(
        "Cerebral Palsy\n\n"
        "A disorder of muscle control or coordination "
        "resulting from injury to the brain."
    )

    chunks, _, _ = chunk_pdf_page(
        page=page,
        source="disabilities.pdf",
        section="Cerebral Palsy",
        chunk_size=100,
        overlap=20,
    )

    assert chunks
    assert chunks[0].source == "disabilities.pdf"
    assert chunks[0].section == "Cerebral Palsy"
    assert chunks[0].pdf_page_number == 4
    assert chunks[0].book_page_number == 16


def test_chunk_ids_are_sequential():
    page = make_page(
        "This is the first paragraph. "
        "It contains some information about the topic.\n\n"
        "This is the second paragraph. "
        "It contains additional information."
    )

    chunks, _, _ = chunk_pdf_page(
        page=page,
        source="disabilities.pdf",
        section="Cerebral Palsy",
        chunk_size=20,
        overlap=5,
    )

    chunk_ids = [
        chunk.chunk_id
        for chunk in chunks
    ]

    assert chunk_ids == list(
        range(len(chunks))
    )


def test_chunks_respect_token_limit():
    page = make_page(
        "This is a sentence about cerebral palsy. "
        "It describes problems with muscle control. "
        "Another sentence provides additional information."
    )

    max_tokens = 20

    chunks, _, _ = chunk_pdf_page(
        page=page,
        source="disabilities.pdf",
        section="Cerebral Palsy",
        chunk_size=max_tokens,
        overlap=5,
    )

    assert chunks

    for chunk in chunks:
        assert count_tokens(
            chunk.text
        ) <= max_tokens


def test_overlap_preserves_context():
    page = make_page(
        "Sentence one contains information about the condition. "
        "Sentence two provides additional clinical information. "
        "Sentence three explains common feeding problems. "
        "Sentence four describes nutritional considerations."
    )

    chunks, _, _ = chunk_pdf_page(
        page=page,
        source="disabilities.pdf",
        section="Cerebral Palsy",
        chunk_size=25,
        overlap=10,
    )

    assert len(chunks) > 1

    first_text = chunks[0].text
    second_text = chunks[1].text

    assert first_text.split()[-1] in second_text


def test_table_is_kept_as_independent_chunk():
    page = DocumentPage(
        elements=[
            DocumentElement(
                text="Table 1. Frequently occurring disabilities",
                element_type="text",
            ),
            DocumentElement(
                text=(
                    "| SYNDROME/DISABILITY | "
                    "Altered Growth | "
                    "Altered Energy Need |\n"
                    "| Cerebral Palsy | "
                    "Underweight | "
                    "Increased calories |"
                ),
                element_type="table",
            ),
        ],
        pdf_page_number=12,
        book_page_number=24,
    )

    chunks, _, _ = chunk_pdf_page(
        page=page,
        source="disabilities.pdf",
        section="Chapter Introduction",
        chunk_size=300,
        overlap=40,
    )

    table_chunks = [
        chunk
        for chunk in chunks
        if "SYNDROME/DISABILITY" in chunk.text
    ]

    assert table_chunks

    assert all(
        chunk.section
        == "Table 1 - Frequently occurring disabilities"
        for chunk in table_chunks
    )
