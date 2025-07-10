# Stable Diffusion 1.5 — Serverless Text‑to‑Image

## The fastest way to turn a prompt into a picture, powered by 🤗 **`runwayml/stable-diffusion-v1-5`** and Modal.

## ⚡️ Quick test (already deployed)

> Replace the prompt and save the PNG — no setup required.

```bash
# Health check
curl https://johnx69--sd15-txt2img-health.modal.run
# Generate an image
curl -X POST https://johnx69--sd15-txt2img-txt2img.modal.run \
     -H "Content-Type: application/json" \
     -d '{
           "prompt": "A photorealistic cat astronaut on the moon",
           "num_inference_steps": 30,
           "guidance_scale": 7.5,
           "height": 512,
           "width": 512
         }' \
     --output moon_cat.png
```

- Cold‑start: ≈ 27 s • warm: ≈ 3.5 s

---

## 🛠️ Local development (CPU)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload      # http://localhost:8000
```

---

## 📦 Docker (optional)

```bash
# Build & run (CPU)
docker build -t sd-api:cpu .
docker run --rm -p 8000:8000 sd-api:cpu
```

## Need GPU? Use `Dockerfile_gpu` + `--gpus all`.

## 🚀 Modal Development & Deployment

### Prerequisites

```bash
# Install Modal CLI
pip install modal
# Authenticate (one-time setup)
modal setup
```

### Local development with Modal (`modal serve`)

Use `modal serve` for rapid development and testing with Modal's infrastructure:

```bash
# Serve the app locally with hot-reloading
modal serve modal_app.py
```

This command:

- 🔄 **Hot-reloads** on file changes (no need to redeploy)
- 🌐 **Exposes local endpoints** (usually `https://yourname--sd15-txt2img-{function}.modal.run`)
- ⚡ **Uses Modal's GPU infrastructure** (faster than local CPU)
- 🧪 **Perfect for testing** before production deployment

### Production deployment (`modal deploy`)

When ready for production:

```bash
# Deploy to production
modal deploy modal_app.py --name sd15-txt2img
```

This command:

- 🚀 **Creates stable production endpoints**
- 📈 **Enables auto-scaling** based on traffic
- 🔒 **Locks in the current code version**
- 🌍 **Production-ready** with persistent URLs

**Key differences:**
| Command | Use Case | URL Stability | Hot Reload |
|---------|----------|---------------|------------|
| `modal serve` | Development & testing | Temporary dev URLs | ✅ Yes |
| `modal deploy` | Production | Permanent production URLs | ❌ No |

### Configuration Tips

```python
# In modal_app.py, you can customize:
@app.function(
    gpu="A10G",              # GPU type (A10G, A100, T4, etc.)
    timeout=300,             # Max execution time
    container_idle_timeout=240,  # Scale-down delay
    allow_concurrent_inputs=10   # Concurrent requests
)
```

---

## 🎯 API reference

| Method | Path       | Description                |
| ------ | ---------- | -------------------------- |
| GET    | `/health`  | Service health check       |
| POST   | `/txt2img` | Generate image from prompt |

```jsonc
{
  "prompt": "string", // required
  "negative_prompt": "string", // optional
  "num_inference_steps": 30,
  "guidance_scale": 7.5,
  "height": 512,
  "width": 512
}
```

---

### Extra notes

- Weights are cached in a Modal **Volume** → no egress fees, fast cold‑starts.
- Adjust `container_idle_timeout` in **`modal_app.py`** to tune idle‑shutdown.
- Local, Docker and Modal paths are identical, so you can swap environments freely.
- Use `modal serve` during development, `modal deploy` for production.
