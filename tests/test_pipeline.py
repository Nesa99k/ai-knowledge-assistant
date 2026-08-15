from app.ingestion.pipeline import ingest_pdf


PDF_PATH = "data/documents/disabilities.pdf"


def test_ingest_real_document():
    chunks = ingest_pdf(
        PDF_PATH,
        chunk_size=300,
    )

    assert chunks

    assert all(
        chunk.source == PDF_PATH
        for chunk in chunks
    )

    assert all(
        chunk.text.strip()
        for chunk in chunks
    )


def test_ingest_real_document_preserves_page_metadata():
    chunks = ingest_pdf(
        PDF_PATH,
        chunk_size=300,
    )

    assert all(
        chunk.pdf_page_number > 0
        for chunk in chunks
    )

    numbered_chunks = [
        chunk
        for chunk in chunks
        if chunk.book_page_number is not None
    ]

    assert numbered_chunks

    assert all(
        chunk.book_page_number >= 15
        for chunk in numbered_chunks
    )


def test_ingest_pdf_preserves_section_across_pages():
    chunks = ingest_pdf(
        PDF_PATH,
        chunk_size=300,
        overlap=40,
    )

    assert chunks

    cerebral_palsy_chunks = [
        chunk
        for chunk in chunks
        if chunk.section == "Cerebral Palsy"
    ]

    assert cerebral_palsy_chunks


def test_chunk_ids_are_continuous():
    chunks = ingest_pdf(
        PDF_PATH,
        chunk_size=300,
        overlap=40,
    )

    chunk_ids = [
        chunk.chunk_id
        for chunk in chunks
    ]

    assert chunk_ids == list(
        range(len(chunks))
    )


def test_table_has_its_own_section():
    chunks = ingest_pdf(
        PDF_PATH,
        chunk_size=300,
        overlap=40,
    )

    table_chunks = [
        chunk
        for chunk in chunks
        if chunk.section
        == "Table 1 - Frequently occurring disabilities"
    ]

    assert table_chunks

    assert any(
        chunk.pdf_page_number == 12
        for chunk in table_chunks
    )

    assert any(
        chunk.pdf_page_number == 13
        for chunk in table_chunks
    )
