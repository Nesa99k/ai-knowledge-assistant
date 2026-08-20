from app.llm.query_rewriter import QueryRewriter


def test_empty_user_query_returns_empty_string():
    rewriter = QueryRewriter()

    result = rewriter.rewrite("")

    assert result == ""


def test_whitespace_query_returns_empty_string():
    rewriter = QueryRewriter()

    result = rewriter.rewrite("   ")

    assert result == ""


def test_empty_rewrite_falls_back_to_original_query(
    monkeypatch,
):
    rewriter = QueryRewriter()

    monkeypatch.setattr(
        rewriter.llm,
        "generate",
        lambda prompt: "",
    )

    original_query = (
        "What is the recommended daily protein "
        "intake for children with cerebral palsy?"
    )

    rewritten_query = rewriter.rewrite(
        original_query
    )

    assert rewritten_query == original_query
