from datetime import datetime
from typing import List
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

from app.evaluation.ragas_evaluator import RAGASEvaluator
load_dotenv()

from .retriever import RAGRetriever
from app.prompt.prompt_loader import PromptLoader
from app.evaluation.evaluation_store import MongoEvaluationStore
from app.observability.logging import get_logger
from app.observability.metrics import EvaluationMetrics
from app.observability.tracing import start_rag_span



class RAGPipeline:
    def __init__(
        self,
        pg_dsn: str,
        mongo_uri: str,
        data_dir: str = "data/documents",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        llm_model: str = "gpt-4o-mini"
    ):
        self.retriever = RAGRetriever(
            pg_dsn=pg_dsn,
            data_dir=data_dir,
            embedding_model=embedding_model
        )

        self.llm = ChatOpenAI(
            model=llm_model,
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        self.prompt_loader = PromptLoader(pg_dsn)
        self.evaluation_store = MongoEvaluationStore(mongo_uri)

        self.judge = LLMJudge()
        self.ragas = RAGASEvaluator()

        self.logger = get_logger("RAGPipeline")
        self.metrics = EvaluationMetrics()

        print("Mongo connected:", self.evaluation_store.db.name)




    async def initialize(self):
        await self.retriever.initialize()

    async def ingest(self):
        return await self.retriever.ingest_documents()

    async def run(self, query: str) -> Dict[str, Any]:
        with start_rag_span("rag_query"):
            start_time = time.time()

            # 1. Retrieve documents
            docs: List[Document] = await self.retriever.search(query)
            sources = [d.page_content for d in docs]
            context = "\n\n".join(sources)

            # 2. Load latest prompt version
            prompt_text = await self.prompt_loader.load("rag_system_prompt")

            prompt = PromptTemplate(
                input_variables=["context", "query"],
                template=prompt_text
            )

            final_prompt = prompt.format(context=context, query=query)

            # 3. LLM call
            response = self.llm.invoke(final_prompt)
            answer = response.content

            # 4. Compute latency
            latency_ms = (time.time() - start_time) * 1000

            # 5. Evaluate answer (async)
            evaluation = await self._evaluate(
                question=query,
                answer=answer,
                docs=sources
            )
            self.logger.info("RAG query completed", extra={"latency_ms": latency_ms})

            # 6. Inject runtime metrics
            evaluation["latency_ms"] = latency_ms
            evaluation["throughput"] = 1.0  # placeholder
            self.logger.info("Evaluation stored", extra={"judge_score": evaluation["judge_score"]})

            # 7. Final combined response
            return {
                "answer": answer,
                "sources": sources,
                "judge_score": evaluation["judge_score"],
                "ragas_scores": evaluation["ragas_scores"],
                "drift": evaluation["drift"],
                "latency_ms": evaluation["latency_ms"],
                "throughput": evaluation["throughput"]
            }


    async def close(self):
        await self.retriever.close()
        
    # -------------------------------------------------------------
    # Evaluation placeholder
    # This will later:
    # - Run LLM-as-judge
    # - Compute RAGAS metrics
    # - Detect drift (data / concept / prediction)
    # - Measure latency / throughput
    # - Save results to MongoEvaluationStore
    # For now, it only returns a structured placeholder.
    # -------------------------------------------------------------
    async def _evaluate(self, question: str, answer: str, docs: List[str]) -> Dict[str, Any]:
        context = "\n\n".join(docs)

        # 1. LLM-as-judge
        judge_raw = await self.judge.score(
            question=question,
            answer=answer,
            context=context
        )

        score = None
        justification = ""

        for line in judge_raw.split("\n"):
            if "score" in line.lower():
                score = float(line.split(":")[1].strip().split("/")[0])
            if "justification" in line.lower():
                justification = line.split(":", 1)[1].strip()

        # 2. RAGAS evaluation
        ragas_dataset = {
            "question": [question],
            "answer": [answer],
            "contexts": [docs]
        }

        ragas_result = await self.ragas.run(ragas_dataset)

        ragas_scores = {
            "faithfulness": ragas_result["faithfulness"][0],
            "answer_relevance": ragas_result["answer_relevance"][0],
            "context_precision": ragas_result["context_precision"][0],
            "context_recall": ragas_result["context_recall"][0]
        }

        # 3. Drift metrics (align with your spec)
        drift = {
            "embedding_shift": 0.02,
            "semantic_shift": 0.03
        }

        # 4. Performance metrics (latency injected in run())
        latency_ms = None
        throughput = None

        # 5. Build evaluation record
        record = EvaluationRecord(
            question=question,
            answer=answer,
            sources=docs,
            judge_score=score,
            judge_justification=justification,
            ragas_scores=ragas_scores,
            drift=drift,
            latency_ms=latency_ms,
            throughput=throughput,
            created_at=datetime.utcnow()
        )

        self.metrics.add_judge_score(score)
        self.logger.info(
            "Judge score recorded",
            extra={"judge_score": score, "avg_judge_score": self.metrics.avg_judge_score}
        )
        
        # 6. Save AFTER all metrics are computed
        await self.evaluation_store.save(record)


        # 7. Return evaluation summary
        return {
            "judge_score": score,
            "ragas_scores": ragas_scores,
            "drift": drift,
            "latency_ms": latency_ms,
            "throughput": throughput,
            "sources": docs
        }




