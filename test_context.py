from app.llm.context import build_context
from app.ingestion.retriever import Retriever


query = (
    "What are the feeding problems associated "
    "with cerebral palsy?"
)


retriever = Retriever(
    top_k=5,
    similarity_threshold=0.75,
)

results = retriever.retrieve(
    query
)

context = build_context(
    results
)


print("\n" + "=" * 80)
print("RETRIEVED CONTEXT")
print("=" * 80)

print(context)
