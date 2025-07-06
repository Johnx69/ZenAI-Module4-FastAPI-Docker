# Stable Diffusion 1.5 FastAPI Service

A minimal web service that exposes a **/txt2img** endpoint backed by the
`runwayml/stable-diffusion-v1-5` model from 🤗 Diffusers.

## Quick start (local, no Docker)

```bash
# 1. Create a venv
python -m venv .venv && source .venv/bin/activate

# 2. Install deps (CPU)
pip install --upgrade pip
pip install -r requirements.txt

# 3. Run
uvicorn app.main:app --host 0.0.0.0 --reload
```

---

## 🐳 Docker Compose (Recommended)

> **The easiest way to run the full stack with nginx reverse proxy**

### 1. Run the full stack

```bash
# Start the service with nginx proxy
docker-compose up --build

# Or run in background
docker-compose up --build -d
```

### 2. Test through nginx (port 80)

```bash
curl -X POST http://localhost/txt2img \
     -H "Content-Type: application/json" \
     -d '{
           "prompt": "A photorealistic cat astronaut on the moon",
           "num_inference_steps": 25,
           "guidance_scale": 8.0,
           "height": 512,
           "width": 512
         }' \
     --output moon_cat.png
```

### 3. Health checks

```bash
# Check nginx health
curl http://localhost/_nginx_health

# Check API health (through nginx)
curl http://localhost/health
```

### 4. GPU support with docker-compose

To enable GPU support, uncomment the GPU section in `docker-compose.yml`:

```yaml
deploy:
  resources:
    reservations:
      devices:
        - capabilities: [gpu]
```

Then rebuild:

```bash
docker-compose down
docker-compose up --build
```

### 5. Stop the services

```bash
# Stop gracefully
docker-compose down

# Stop and remove volumes/images
docker-compose down -v --rmi all
```

---

## 🔧 Manual Docker usage

> **For advanced users who want more control**

### 1. Build the image

#### CPU‑only (lightweight but slower)

```bash
docker build -t sd-api:cpu -f Dockerfile .
```

#### GPU (CUDA 11.8, much faster)

```bash
docker build -t sd-api:gpu -f Dockerfile_gpu .
```

### 2. Run the container

#### CPU container

```bash
docker run --rm -p 8000:8000 sd-api:cpu
```

#### GPU container

```bash
docker run --gpus all --rm -p 8000:8000 sd-api:gpu
```

### 3. Test the endpoint (direct to API)

```bash
curl -X POST http://localhost:8000/txt2img \
     -H "Content-Type: application/json" \
     -d '{
           "prompt": "A photorealistic cat astronaut on the moon",
           "num_inference_steps": 25,
           "guidance_scale": 8.0,
           "height": 512,
           "width": 512
         }' \
     --output moon_cat.png
```

---

## 🎯 API Endpoints

| Endpoint         | Method | Description                              |
| ---------------- | ------ | ---------------------------------------- |
| `/health`        | GET    | Service health check                     |
| `/txt2img`       | POST   | Generate image from text prompt          |
| `/_nginx_health` | GET    | Nginx health check (docker-compose only) |

### Request Parameters

```json
{
  "prompt": "string (required)",
  "negative_prompt": "string (optional)",
  "num_inference_steps": 30,
  "guidance_scale": 7.5,
  "height": 512,
  "width": 512
}
```
