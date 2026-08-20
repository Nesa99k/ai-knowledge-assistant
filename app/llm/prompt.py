def build_rag_prompt(
    question: str,
    context: str,
) -> str:
    """Build a grounded prompt for RAG question answering."""

    return f"""You are a question-answering assistant for a document-based knowledge system.

Answer the user's question using ONLY the information provided in the context below.

Rules:
- Use only information explicitly stated in the context.
- Do not use outside knowledge or assumptions.
- Focus on information that directly answers the question.
- If the context contains a section titled "What to expect in the Diet Prescription" or "What to Expect in the Diet Prescription", treat it as especially relevant to questions about dietary considerations.
- Preserve the specific dietary recommendations stated in the context.
- Do not replace specific recommendations with general medical knowledge.
- If multiple relevant chunks are provided, combine their information into one concise answer.
- Do not repeat irrelevant background information.
- If the requested information is not present in the context, say that it is not available in the provided document.

Context:
{context}

Question:
{question}

Answer:
"""
