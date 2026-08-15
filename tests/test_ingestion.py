from app.ingestion.pipeline import ingest_pdf


def test_ingest_real_document():
    chunks = ingest_pdf(
        "data/documents/disabilities.pdf",
        chunk_size=300,
    )

    assert chunks

    assert all(
        chunk.source == "data/documents/disabilities.pdf"
        for chunk in chunks
    )

    assert all(
        chunk.text.strip()
        for chunk in chunks
    )
