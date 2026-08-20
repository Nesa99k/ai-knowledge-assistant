from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

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
        answer = rag_pipeline.answer(
            request.question,
            section=request.section,
        )

        return AskResponse(answer=answer)

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing the question.",
        )


@router.post("/ask/stream")
def ask_stream(request: AskRequest):

    def generate():
        try:
            for chunk in rag_pipeline.answer_stream(
                request.question,
                section=request.section,
            ):
                yield chunk.replace("\n", "\\n") + "\n"

        except Exception:
            yield "[ERROR]\n"

    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
