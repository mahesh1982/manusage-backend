# app/evaluation/evaluation_store.py

from datetime import datetime
from pydantic import BaseModel
from typing import Dict, List

from app.memory.mongo_store import MongoConnection


class EvaluationRecord(BaseModel):
    """
    Represents one evaluation event.
    This is the document we store in MongoDB.
    """
    question: str
    answer: str
    sources: List[str]
    judge_score: float
    judge_justification: str
    ragas_scores: Dict[str, float]
    created_at: datetime


class MongoEvaluationStore:
    """
    Handles ONLY evaluation storage.
    Uses MongoConnection to talk to MongoDB.
    """
    def __init__(self, mongo_uri: str):
        # Create a connection object
        self.connection = MongoConnection(mongo_uri)

        # Get the database
        self.db = self.connection.get_db()

        # Select the collection (auto-created if not exists)
        self.collection = self.db["evaluations"]

    def save(self, record: EvaluationRecord):
        """
        Insert the evaluation record into MongoDB.
        """
        doc = record.dict()
        result = self.collection.insert_one(doc)
        return str(result.inserted_id)
