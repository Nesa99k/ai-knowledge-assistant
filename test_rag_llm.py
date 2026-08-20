from app.llm.rag import RAGPipeline


QUESTIONS = [
    # 1. سؤال ساده و مستقیم
    "What are the feeding problems associated with cerebral palsy?",

    # 2. سؤال با wording متفاوت
    "What difficulties can children with CP have when eating?",

    # 3. سؤال درباره جدول
    "According to Table 1, what feeding problems are listed for Down Syndrome?",

    # 4. سؤال خارج از اطلاعات موجود در context
    "What is the recommended daily protein intake for children with cerebral palsy?",
]


rag = RAGPipeline(
    top_k=5,
    similarity_threshold=0.75,
)


for question in QUESTIONS:

    print("\n\n" + "=" * 80)
    print("QUESTION")
    print("=" * 80)
    print(question)

    answer = rag.answer(
        question
    )

    print("\n" + "=" * 80)
    print("RAG ANSWER")
    print("=" * 80)
    print(answer)
