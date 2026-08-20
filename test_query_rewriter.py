from app.llm.query_rewriter import QueryRewriter


rewriter = QueryRewriter()


QUESTIONS = [
    "What are the feeding problems associated with cerebral palsy?",
    "What difficulties can children with CP have when eating?",
    "What nutrition problems are associated with epilepsy?",
    "According to Table 1, what feeding problems are listed for Down Syndrome?",
    "What is the recommended daily protein intake for children with cerebral palsy?",
]


for question in QUESTIONS:

    rewritten_query = rewriter.rewrite(
        question
    )

    print("\n" + "=" * 80)
    print("ORIGINAL QUERY")
    print("=" * 80)
    print(question)

    print("-" * 80)
    print("REWRITTEN QUERY")
    print("-" * 80)
    print(rewritten_query)
