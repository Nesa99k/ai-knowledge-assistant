from app.ingestion.retriever import Retriever
from app.llm.context import build_context
from app.llm.prompt import build_rag_prompt
from app.llm.client import LLMClient


class RAGPipeline:
    """End-to-end retrieval-augmented generation pipeline."""

    def __init__(self,
                 top_k: int = 5,
                 similarity_threshold: float = 0.75,
                 ) -> None:
        self.retriever = Retriever(
            top_k=top_k,
            similarity_threshold=similarity_threshold,
        )
        self.llm = LLMClient()

    def answer(
        self,
        question: str,
    ) -> str:
        """Retrieve relevant context and generate an answer."""

        results = self.retriever.retrieve(question)

        if not results:
            return (
                "I could not find relevant information "
                "in the provided document."
            )
        context = build_context(results)

        prompt = build_rag_prompt(
            question=question,
            context=context,
        )
        return self.llm.generate(prompt)
