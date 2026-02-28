from pydantic import BaseModel, Field

class QueryInput(BaseModel):
    query: str = Field(..., min_length=2, max_length=500)
    prompt_name: str = "rag_system_prompt"
