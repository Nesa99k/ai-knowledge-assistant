from app.ingestion.retriever import Retriever


QUERY = (
    "What are the feeding problems associated "
    "with cerebral palsy?"
)


retriever = Retriever(
    top_k=5,
    similarity_threshold=0.75,
)

results = retriever.retrieve(
    QUERY
)


print("\n" + "=" * 80)
print("RETRIEVAL RESULTS")
print("=" * 80)


if not results:
    print(
        "No results passed "
        "the similarity threshold."
    )
    raise SystemExit


for result in results:
    chunk = result["chunk"]

    print("=" * 80)
    print(
        f"Similarity: "
        f"{result['similarity']:.4f}"
    )
    print(
        f"Chunk ID: "
        f"{chunk['chunk_id']}"
    )
    print(
        f"Section: "
        f"{chunk['section']}"
    )
    print(
        f"PDF page: "
        f"{chunk['pdf_page_number']}"
    )
    print(
        f"Book page: "
        f"{chunk['book_page_number']}"
    )
    print("-" * 80)
    print(chunk["text"])
