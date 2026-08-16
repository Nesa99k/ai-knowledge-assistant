from app.ingestion.loader import load_pdf
from app.ingestion.chunker import chunk_pdf_page


pages = load_pdf(
    "data/documents/disabilities.pdf"
)

all_chunks = []

current_section = "Chapter Introduction"
next_chunk_id = 0

for page in pages:

    chunks, current_section, next_chunk_id = (
        chunk_pdf_page(
            page=page,
            source="disabilities.pdf",
            section=current_section,
            chunk_size=300,
            overlap=40,
            start_chunk_id=next_chunk_id,
        )
    )

    all_chunks.extend(chunks)


print(f"Total pages: {len(pages)}")
print(f"Total chunks: {len(all_chunks)}")

for chunk in all_chunks:

    print("=" * 80)
    print(
        f"Chunk ID: {chunk.chunk_id} | "
        f"PDF page: {chunk.pdf_page_number} | "
        f"Book page: {chunk.book_page_number}"
    )

    print(
        f"Section: {chunk.section}"
    )

    print("-" * 80)
    print(chunk.text[:500])
