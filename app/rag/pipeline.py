from typing import List
from langchain.schema import Document
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

from .retriever import RAGRetriever
from app.prompt.prompt_loader import PromptLoader


class RAGPipeline:
    def __init__(
        self,
        pg_dsn: str,
        data_dir: str = "data/documents",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        llm_model: str = "gpt-4o-mini"
    ):
        self.retriever = RAGRetriever(
            pg_dsn=pg_dsn,
            data_dir=data_dir,
            embedding_model=embedding_model
        )

        self.llm = ChatOpenAI(model=llm_model, temperature=0)

        # FIXED: removed extra parenthesis
        self.prompt_loader = PromptLoader(pg_dsn)

    async def initialize(self):
        await self.retriever.initialize()

    async def ingest(self):
        return await self.retriever.ingest_documents()

    async def run(self, query: str) -> str:
        docs: List[Document] = await self.retriever.search(query)
        context = "\n\n".join([d.page_content for d in docs])

        # Load latest prompt version from PostgreSQL
        prompt_text = await self.prompt_loader.load("rag_system_prompt")

        prompt = PromptTemplate(
            input_variables=["context", "query"],
            template=prompt_text
        )

        final_prompt = prompt.format(context=context, query=query)

        # LLM call
        response = self.llm.invoke(final_prompt)

        return response.content

    async def close(self):
        await self.retriever.close()
