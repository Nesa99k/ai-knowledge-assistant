from app.ingestion.vector_store import (
    build_index,
    load_embeddings,
    save_index,
)


chunks, embeddings = load_embeddings(
    "data/processed/disabilities_embeddings.json"
)

index = build_index(embeddings)

save_index(
    index,
    "data/processed/disabilities.index",
)

print("FAISS index created successfully.")
print(f"Vectors: {index.ntotal}")
print(f"Dimension: {index.d}")
