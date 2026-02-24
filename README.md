# 🧠 ManusAge — Document Age Estimation Backend

ManusAge is a modular, production‑grade GenAI system designed to estimate the age of handwritten or printed documents using a combination of:

- Vision models  
- RAG pipelines  
- LLM reasoning  
- Metadata analysis  
- Agentic orchestration  

This repository contains the **backend microservice**, built with FastAPI and deployed using Docker + Azure Container Apps.

---

## 🚀 Features

- FastAPI‑based microservice architecture  
- Health endpoint for monitoring  
- Dockerized for reproducible builds  
- AMD64‑compatible images for cloud deployment  
- Azure Container Registry (ACR) integration  
- Azure Container Apps deployment  
- Scale‑to‑zero support for cost‑efficient hosting  
- Clean project structure for future RAG + Vision integration  

---

## 🏗️ Architecture Overview

manusage-backend/
│
├── app/
│   ├── main.py          # FastAPI entrypoint
│   ├── config.py        # Pydantic settings (v2)
│   ├── routes/          # API endpoints (future expansion)
│   └── services/        # Business logic modules
│
├── Dockerfile           # AMD64-compatible container build
├── requirements.txt     # Python dependencies
├── DEPLOYMENT.md        # Azure deployment guide
└── README.md            # Project documentation


---

## 🧪 Local Development

### 1. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000


http://localhost:8000/health

docker buildx build --platform linux/amd64 -t manusage-backend-amd64 .

docker run -p 8000:8000 manusage-backend-amd64

docker tag manusage-backend-amd64 manusageacr.azurecr.io/manusage-backend:latest
docker push manusageacr.azurecr.io/manusage-backend:latest


az containerapp create \
  --name manusage-backend \
  --resource-group manusage-rg \
  --environment manusage-env \
  --image manusageacr.azurecr.io/manusage-backend:latest \
  --target-port 8000 \
  --ingress external \
  --registry-server manusageacr.azurecr.io


https://<your-app>.azurecontainerapps.io/health

az containerapp update \
  --name manusage-backend \
  --resource-group manusage-rg \
  --min-replicas 0 \
  --max-replicas 1

📄 License
This project is for educational and portfolio purposes.
---
👤 Author
Maheswara Reddy
GenAI Engineer | RAG Systems | Agentic Architectures
