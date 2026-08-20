from app.ingestion.retriever import Retriever


retriever = Retriever(
    top_k=5,
    similarity_threshold=0.75,
)


QUESTION = (
    "What are the feeding problems associated "
    "with cerebral palsy?"
)


print("\n" + "=" * 80)
print("WITHOUT METADATA FILTER")
print("=" * 80)

results = retriever.retrieve(
    query=QUESTION,
)

for result in results:
    chunk = result["chunk"]

    print("-" * 80)
    print(
        f"Similarity: "
        f"{result['similarity']:.4f}"
    )
    print(
        f"Section: "
        f"{chunk['section']}"
    )
    print(
        f"Chunk ID: "
        f"{chunk['chunk_id']}"
    )


print("\n" + "=" * 80)
print("WITH SECTION FILTER")
print("=" * 80)

results = retriever.retrieve(
    query=QUESTION,
    section="Cerebral Palsy",
)

for result in results:
    chunk = result["chunk"]

    print("-" * 80)
    print(
        f"Similarity: "
        f"{result['similarity']:.4f}"
    )
    print(
        f"Section: "
        f"{chunk['section']}"
    )
    print(
        f"Chunk ID: "
        f"{chunk['chunk_id']}"
    )
