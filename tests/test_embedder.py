from app.ingestion.embedder import embed_text


def test_embed_text_returns_vector():

    text = "Cerebral palsy is a disorder of muscle control."

    embedding = embed_text(text)

    assert embedding
    assert len(embedding) == 384
    assert all(isinstance(value, float) for value in embedding)
