from app.ingestion.embedding_pipeline import embed_chunks

embed_chunks(
    input_path="data/processed/disabilities_chunks.json",
    output_path="data/processed/disabilities_embeddings.json",
)
print("Embeddings created successfully.")
