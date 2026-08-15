from app.ingestion.pipeline import ingest_document
from app.ingestion.chunker import count_tokens, chunk_markdown

chunks = ingest_document(
    "data/documents/huggingface_rag.md",
    chunk_size=300,
    overlap=50,
)

print(f"Total chunks:{len(chunks)}")

for chunk in chunks:
    print("-" * 60)
    print(f"Chunk ID: {chunk.chunk_id}")
    print(f"Source: {chunk.source}")
    print(f"Section: {chunk.section}")
    print(f"Tokens: {count_tokens(chunk.text)}")
    print(f"Text: {chunk.text[:300]}...")
