from fastapi import APIRouter
from app.rag.pipeline import RAGPipeline
import os

router = APIRouter()

PG_DSN = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

pipeline = RAGPipeline(pg_dsn=PG_DSN)


@router.post("/ingest")
def ingest_documents():
    pipeline.ingest()
    return {"status": "ok"}

@router.post("/query")
def query_rag(payload: dict):
    query = payload.get("query")
    prompt_name = payload.get("prompt_name", "rag_system_prompt")
    answer, context = pipeline.query(query=query, prompt_name=prompt_name)
    return {"answer": answer, "context": context}
