# Stable Diffusion 1.5 FastAPI Service

A minimal web service that exposes a **/txt2img** endpoint backed by the
`runwayml/stable-diffusion-v1-5` model from 🤗 Diffusers.

---

## Features

- 🔌 **FastAPI + Uvicorn** – simple, async‑compatible REST API
- 🏗️ **Docker‑first** – CPU & GPU Dockerfiles provided
- 🔒 **CORS** enabled (configured to `*` for dev; restrict in prod)
- 🖼️ Streams raw PNG bytes for immediate browser display

---

## Quick start (local, no Docker)

```bash
# 1. Create a venv
python -m venv .venv && source .venv/bin/activate

# 2. Install deps (CPU)
pip install --upgrade pip
pip install -r requirements.txt

# 3. Run
uvicorn app.main:app --reload
# → Service at http://localhost:8000
```

---

## Docker usage

> **Prerequisites**
>
> - Docker ≥ 20.10
> - (GPU build) NVIDIA driver ≥ 525 **+** nvidia‑container‑toolkit
> - (Private or gated models) a valid Hugging Face token exported as `HF_TOKEN`

### 1. Build the image

#### CPU‑only (lightweight but slower)

```bash
docker build -t sd-api:cpu -f Dockerfile .
```

#### GPU (CUDA 11.8, much faster)

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

### 3. Test the endpoint

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
