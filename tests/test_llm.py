from app.llm.client import LLMClient
from unittest.mock import Mock


def test_llm_client_creation():
    llm = LLMClient()
    assert llm is not None


def test_llm_generate():
    llm = LLMClient()
    fake_response = Mock()
    fake_response.output_text = "This is a fake LLM response."
    llm.client.responses.create = Mock(return_value=fake_response)
    answer = llm.generate("What is RAG?")
    assert answer == "This is a fake LLM response."
    assert llm is not None
