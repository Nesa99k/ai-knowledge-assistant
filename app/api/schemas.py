from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=1)
    section: str | None = None


class AskResponse(BaseModel):
    answer: str
