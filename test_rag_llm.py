from app.llm.rag import RAGPipeline


QUESTION = (
    """According to Table 1, what feeding problems are listed for Cerebral Palsy?"""
)


rag = RAGPipeline(
    top_k=5,
    similarity_threshold=0.75,
)

answer = rag.answer(
    QUESTION
)


print("\n" + "=" * 80)
print("RAG ANSWER")
print("=" * 80)
print(answer)
