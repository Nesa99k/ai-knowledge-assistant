from app.ingestion.retriever import Retriever
from app.llm.context import build_context
from app.llm.prompt import build_rag_prompt
from app.llm.client import LLMClient
from app.llm.query_rewriter import QueryRewriter


class RAGPipeline:
    """End-to-end retrieval-augmented generation pipeline."""

    def __init__(self,
                 top_k: int = 5,
                 similarity_threshold: float = 0.75,
                 section_similarity_threshold: float = 0.60,
                 ) -> None:
        self.rewriter = QueryRewriter()

        self.retriever = Retriever(
            top_k=top_k,
            similarity_threshold=similarity_threshold,
            section_similarity_threshold=section_similarity_threshold,
        )
        self.llm = LLMClient()

    def answer(
        self,
        question: str,
        section: str | None = None,
    ) -> str:
        """Answer a question using retrieved document context."""
        retrieval_query = question

        print("\n" + "=" * 80)
        print("QUERY REWRITING")
        print("=" * 80)
        print(f"Original: {question}")
        print(f"Rewritten: {retrieval_query}")

        results = self.retriever.retrieve(
            retrieval_query,
            section=section,
        )

        print("\n" + "=" * 80)
        print("RETRIEVED CHUNKS")
        print("=" * 80)

        if not results:
            return (
                "I could not find relevant information "
                "in the provided document."
            )
        for result in results:
            chunk = result["chunk"]

            print("-" * 80)
            print(f"Similarity: {result['similarity']:.4f}")
            print(f"Section: {chunk['section']}")
            print(f"Chunk ID: {chunk['chunk_id']}")

        context = build_context(results)

        print("\n" + "=" * 80)
        print("FINAL CONTEXT")
        print("=" * 80)
        print(context)

        prompt = build_rag_prompt(
            question=question,
            context=context,
        )
        return self.llm.generate(prompt)
