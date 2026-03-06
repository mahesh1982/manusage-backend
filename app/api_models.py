from pydantic import BaseModel
from typing import Optional, Dict, List

class RAGResponse(BaseModel):
    answer: str
    sources: Optional[List[str]]
    judge_score: Optional[float]
    ragas_scores: Optional[Dict[str, float]]
    drift: Optional[Dict[str, float]]
    latency_ms: Optional[float]
    throughput: Optional[float]
