from fastapi import APIRouter
import asyncio

from app.rag.pipeline import RAGPipeline
from app.api_models import RAGResponse
from app.config import settings
import os

router = APIRouter()

PG_DSN = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

pipeline = RAGPipeline(
    pg_dsn=PG_DSN,
    mongo_uri=settings.MONGO_URI
)

@router.post("/ingest")
def ingest_documents():
    result = asyncio.run(pipeline.ingest())
    return {"ingested": result}

@router.post("/query", response_model=RAGResponse)
def query_rag(payload: dict):
    query = payload.get("query")
    result = asyncio.run(pipeline.run(query))
    return result
