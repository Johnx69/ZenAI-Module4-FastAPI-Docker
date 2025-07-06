from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from diffusers import StableDiffusionPipeline
from .models import SDRequest
from fastapi.middleware.cors import CORSMiddleware
import torch, io, os

app = FastAPI(title="SD-1.5 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_ID = "runwayml/stable-diffusion-v1-5"
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID, torch_dtype=dtype, safety_checker=None
).to(device)


# ── Endpoint ───────────────────────────────────────────────────────
@app.post("/txt2img")
def txt2img(req: SDRequest):
    try:
        with torch.inference_mode():
            image = pipe(
                prompt=req.prompt,
                negative_prompt=req.negative_prompt,
                num_inference_steps=req.num_inference_steps,
                guidance_scale=req.guidance_scale,
                height=req.height,
                width=req.width,
            ).images[0]

        buf = io.BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
