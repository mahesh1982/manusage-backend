from pydantic import BaseModel

class RAGOutput(BaseModel):
    answer: str
    sources: list
