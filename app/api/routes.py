from fastapi import APIRouter, HTTPException

from app.api.schemas import AskRequest, AskResponse
from app.llm.rag import RAGPipeline


router = APIRouter()

rag_pipeline = RAGPipeline()


@router.get("/")
def root():
    return {"message": "AI Knowledge Assistant API is running."}


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):

    try:
        answer = rag_pipeline.answer(request.question)

        return AskResponse(answer=answer)

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing the question."
        )
