# 🚀 ManusAge Backend — Deployment Guide

This document describes the full deployment workflow for the ManusAge backend using:

- Docker
- Azure Container Registry (ACR)
- Azure Container Apps (ACA)
- Scale-to-zero configuration for cost efficiency

---

## 📦 1. Build the Docker Image (Local)

```bash
docker buildx build --platform linux/amd64 -t manusage-backend-amd64 .
```

Verify the image:

```bash
docker images
```

---

## 🏷️ 2. Tag the Image for Azure Container Registry

Replace `manusageacr` with your actual ACR name.

```bash
docker tag manusage-backend-amd64 manusageacr.azurecr.io/manusage-backend:latest
```

---

## 📤 3. Push the Image to ACR

```bash
docker push manusageacr.azurecr.io/manusage-backend:latest
```

---

## 🌐 4. Create Azure Resources

### Resource Group

```bash
az group create \
  --name manusage-rg \
  --location eastus
```

### Container Apps Environment

```bash
az containerapp env create \
  --name manusage-env \
  --resource-group manusage-rg \
  --location eastus
```

---

## 🚀 5. Deploy the Container App

```bash
az containerapp create \
  --name manusage-backend \
  --resource-group manusage-rg \
  --environment manusage-env \
  --image manusageacr.azurecr.io/manusage-backend:latest \
  --target-port 8000 \
  --ingress external \
  --registry-server manusageacr.azurecr.io \
  --query properties.configuration.ingress.fqdn
```

This command outputs the public URL of the API.

Example:

```
"manusage-backend.eastus.azurecontainerapps.io"
```

---

## 🧪 6. Test the Deployment

Open:

```
https://<your-url>/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "ManusAge",
  "environment": "dev"
}
```

---

## 💸 7. Cost Optimization (Scale to Zero)

Azure Container Apps supports scale-to-zero.  
This keeps cost extremely low during development.

```bash
az containerapp update \
  --name manusage-backend \
  --resource-group manusage-rg \
  --min-replicas 0 \
  --max-replicas 1
```

---

## 📴 8. Disable Ingress (Optional Pause)

This makes the API unreachable without deleting it.

```bash
az containerapp ingress disable \
  --name manusage-backend \
  --resource-group manusage-rg
```

---

## ❌ 9. Delete the Container App (Zero Cost)

If you want to completely stop billing:

```bash
az containerapp delete \
  --name manusage-backend \
  --resource-group manusage-rg
```

Your image remains safely stored in ACR.

---

## 📚 Notes

- Azure Container Apps **does not support** `az containerapp stop`
- ACR Basic tier costs ~\$5/month
- Scale-to-zero keeps compute cost near \$0
- Logs may incur small charges (\$1–\$3/month)

---

## ✔ Summary

This deployment pipeline provides:

- Reproducible builds  
- Architecture‑correct AMD64 images  
- Secure ACR storage  
- Serverless-style scale-to-zero hosting  
- Minimal cost during development  

ManusAge backend is now production‑ready and cloud‑deployable.

