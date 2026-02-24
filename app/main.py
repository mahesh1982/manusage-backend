from fastapi import FastAPI
from .logging_config import setup_logging
from .config import Settings

# Initialize logging
setup_logging()

# Load settings
settings = Settings()

app = FastAPI(
    title="ManusAge",
    version="0.0.1",
    description="Minimal deployable ManusAge backend"
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ManusAge",
        "environment": settings.environment
    }


#"manusage-backend.redplant-2a81f7c8.eastus.azurecontainerapps.io"
"""Pause:
    az containerapp stop \
  --name manusage-backend \
  --resource-group manusage-rg
Start:
    az containerapp start \
  --name manusage-backend \
  --resource-group manusage-rg
  
  Delete:
  az containerapp delete \
  --name manusage-backend \
  --resource-group manusage-rg
"""
