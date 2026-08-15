from app.ingestion.pipeline import ingest_pdf
from app.ingestion.storage import save_chunks


chunks = ingest_pdf(
    "data/documents/disabilities.pdf",
    chunk_size=300,
    overlap=40,
)

print("Before save:")
print([
    (chunk.chunk_id, chunk.section)
    for chunk in chunks
])

save_chunks(
    chunks,
    "data/processed/disabilities_chunks.json",
)

print(f"Saved {len(chunks)} chunks.")
