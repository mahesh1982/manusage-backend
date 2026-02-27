import asyncpg
from typing import List, Optional
from langchain.schema import Document

class PostgresVectorStore:
    def __init__(self, dsn: str):
        self.dsn = dsn

    async def connect(self):
        self.conn = await asyncpg.connect(self.dsn)

    async def close(self):
        await self.conn.close()

    async def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            content TEXT,
            metadata JSONB,
            embedding VECTOR(384)  -- adjust based on model dimensions
        );
        """
        await self.conn.execute(query)

    async def add_documents(self, docs: List[Document], embeddings: List[List[float]]):
        for doc, emb in zip(docs, embeddings):
            await self.conn.execute(
                """
                INSERT INTO documents (content, metadata, embedding)
                VALUES ($1, $2, $3)
                """,
                doc.page_content,
                doc.metadata,
                emb
            )

    async def similarity_search(self, query_embedding: List[float], k: int = 5):
        rows = await self.conn.fetch(
            """
            SELECT content, metadata, embedding <-> $1 AS distance
            FROM documents
            ORDER BY embedding <-> $1
            LIMIT $2
            """,
            query_embedding,
            k
        )

        return [
            Document(page_content=row["content"], metadata=row["metadata"])
            for row in rows
        ]
