from app.llm.client import LLMClient


class QueryRewriter:
    """Rewrite user questions into retrieval-friendly queries."""

    def __init__(self) -> None:
        self.llm = LLMClient()

    def rewrite(self, query: str) -> str:
        """Rewrite a user query while preserving retrieval-critical terms."""

        query = query.strip()

        if not query:
            return ""

        prompt = f"""
Rewrite the user's question into a concise search query for retrieving
relevant information from a document.

Rules:
- Preserve the original meaning.
- Preserve ALL important medical and domain-specific terms.
- Preserve the complete disease, disorder, or syndrome name.
- Preserve nutrition-related terms such as diet, dietary, nutrition,
  calories, fiber, fluids, feeding, swallowing, texture, and prescription.
- Preserve terms that describe what information the user is asking for.
- Do not remove a term merely because it appears redundant.
- Do not replace specific medical terms with broader terms.
- Do not add information that is not present in the user's question.
- Do not answer the question.
- Return only the search query.
- Do not use quotation marks.

User question:
{query}
"""

        rewritten_query = self.llm.generate(prompt).strip()

        if not rewritten_query:
            return query

        return rewritten_query
