from typing import List
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from .document_loader import DocumentLoader
from .embeddings import EmbeddingModel
from .vector_store import PostgresVectorStore


class RAGRetriever:
    def __init__(
        self,
        pg_dsn: str,
        data_dir: str = "data/documents",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        self.loader = DocumentLoader(data_dir=data_dir)
        self.embedder = EmbeddingModel(model_name=embedding_model)
        self.vector_store = PostgresVectorStore(dsn=pg_dsn)

    async def initialize(self):
        await self.vector_store.connect()
        await self.vector_store.create_table()

    async def ingest_documents(self):
        docs: List[Document] = self.loader.load()
        texts = [d.page_content for d in docs]

        embeddings = self.embedder.embed_documents(texts)
        await self.vector_store.add_documents(docs, embeddings)

        return len(docs)

    async def search(self, query: str, k: int = 5) -> List[Document]:
        query_embedding = self.embedder.embed_query(query)
        results = await self.vector_store.similarity_search(query_embedding, k=k)
        return results

    async def close(self):
        await self.vector_store.close()
