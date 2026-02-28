
ManusAge — GenAI System for Ink Age Estimation &amp; Document Intelligence
ManusAge is a production‑grade GenAI system that performs ink age estimation, document intelligence, and context‑grounded reasoning using a hybrid of RAG, LLM orchestration, multimodal processing, and agentic workflows.
It is designed as an enterprise‑ready reference architecture for modern GenAI engineering.
---
✨ Key Features
RAG Pipeline (Retrieval‑Augmented Generation)
Uses PostgreSQL + pgvector for document embeddings and GPT‑4o‑mini for grounded answers.
Prompt Governance
Versioned prompts stored in Postgres with activation control.
Agentic Workflows
Summarization, evaluation (RAGAS + LLM‑judge), and multimodal agents.
Multimodal Support
Text, audio, and image processing (future: ink age estimation model).
Memory Architecture
Postgres (primary vector store)
ChromaDB (short‑term memory)
MongoDB Atlas (long‑term metadata)
Production‑Ready Backend
FastAPI, Docker, modular folder structure, and clean separation of concerns.
---
📁 Project Structure
manusage-backend/
│
├── app/
│   ├── main.py
│   ├── rag/
│   │   ├── router.py
│   │   ├── pipeline.py
│   │   ├── retriever.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   └── loader.py
│   ├── prompt/
│   │   ├── seed_prompts.py
│   │   └── prompt_loader.py
│   ├── agents/
│   │   ├── summarizer_agent.py
│   │   ├── evaluator_agent.py
│   │   └── multimodal_agent.py
│   └── utils/
│       └── logger.py
│
├── db/
│   ├── migrations/
│   │   └── 001_init.sql
│   └── run_migrations.py
│
├── Dockerfile
├── requirements.txt
└── MANUSAGE_SPEC.md

---
🧠 Architecture Overview
Core Stack
FastAPI — backend API
PostgreSQL + pgvector — vector store
SentenceTransformers — embeddings
OpenAI GPT‑4o‑mini — LLM
LangChain / LangGraph / Smolagents — orchestration
ChromaDB — short‑term memory
MongoDB Atlas — long‑term metadata
Data Flow
Documents are ingested → chunked → embedded → stored in Postgres.
Query is embedded → nearest neighbors retrieved.
Active system prompt loaded from Postgres.
GPT‑4o‑mini generates grounded response.
Agents optionally perform deeper analysis.
---
🗄️ Database Schema
prompt_versions
Stores all prompt versions with activation flags.
documents
Stores raw text, embeddings, and metadata.
vector extension
pgvector enabled for similarity search.
---
🚀 Getting Started
1. Install dependencies
pip install -r requirements.txt

2. Start PostgreSQL
Local:
brew services start postgresql

Or Docker:
docker run -d \
  --name manusage-db \
  -e POSTGRES_DB=postgres \
  -e POSTGRES_USER=maheswarareddyp \
  -p 5432:5432 \
  postgres:15

3. Run migrations
python db/migrations/run_migrations.py

4. Seed initial prompt
python app/prompt/seed_prompts.py

5. Start the API
uvicorn app.main:app --reload

---
📨 API Endpoints
POST /rag/ingest
Ingests and embeds documents.
POST /rag/query
Runs full RAG pipeline with GPT‑4o‑mini.
POST /agents/summarize
Summarizes long documents.
POST /agents/evaluate
Runs RAG evaluation (RAGAS + LLM‑judge).
POST /agents/multimodal
Handles audio/image workflows.
---
🧪 Example Usage
Ingest documents
curl -X POST http://127.0.0.1:8000/rag/ingest

Query the system
curl -X POST http://127.0.0.1:8000/rag/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How does ink age?", "prompt_name": "rag_system_prompt"}'

---
📈 Roadmap
Phase 1 (Current)
RAG pipeline
Prompt governance
GPT‑4o‑mini integration
Phase 2
Audio transcription (Whisper)
Text‑to‑speech
Phase 3
Vision ingestion
Document image analysis
Phase 4
Custom ink age estimation model
Full multimodal agentic workflow
---
📜 License
No License
