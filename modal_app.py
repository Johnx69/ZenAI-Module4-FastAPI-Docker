import io
from typing import Optional
import modal
from pydantic import BaseModel

base_image = (
    modal.Image.from_registry("pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime")
    .env({"DEBIAN_FRONTEND": "noninteractive", "HF_HUB_DISABLE_SYMLINKS_WARNING": "1"})
    .apt_install("git", "curl", "libgl1", "libglib2.0-0")
    .pip_install(
        "torch==2.1.2",
        "diffusers",
        "transformers==4.53.1",
        "accelerate",
        "xformers==0.0.23.post1",
        "diffusers==0.34.0",
        "fastapi",
        "pydantic",
        extra_index_url="https://download.pytorch.org/whl/cu118",
    )
)

####  Model-weights Volume
model_vol = modal.Volume.from_name("sd15-weights-vol", create_if_missing=True)
MOUNT = "/vol/models"

app = modal.App(
    "sd15-txt2img",
    image=base_image,
)

MODEL_ID = "runwayml/stable-diffusion-v1-5"
pipe = None


def get_pipe():
    """Load SD-1.5 once per container; cache weights in Volume."""
    global pipe
    if pipe is None:
        import torch
        from diffusers import StableDiffusionPipeline

        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if device == "cuda" else torch.float32

        pipe = (
            StableDiffusionPipeline.from_pretrained(
                MODEL_ID,
                torch_dtype=dtype,
                cache_dir=f"{MOUNT}/{MODEL_ID}",  # ← stored in Volume
                safety_checker=None,
            )
            .to(device)
            .to(dtype)
        )
        # first container that downloads commits once
        model_vol.commit()
    return pipe


####  Request schema
class SDRequest(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = None
    num_inference_steps: int = 30
    guidance_scale: float = 7.5
    height: int = 512
    width: int = 512


####  /txt2img endpoint
@app.function(
    gpu="L4",
    timeout=600,
    scaledown_window=120,
    volumes={MOUNT: model_vol},  # attach Volume
)
@modal.fastapi_endpoint(method="POST")
def txt2img(req: SDRequest):
    import torch
    from fastapi.responses import Response

    gen = get_pipe()

    with torch.inference_mode():
        img = gen(
            prompt=req.prompt,
            negative_prompt=req.negative_prompt,
            num_inference_steps=req.num_inference_steps,
            guidance_scale=req.guidance_scale,
            height=req.height,
            width=req.width,
        ).images[0]

    buf = io.BytesIO()
    img.save(buf, "PNG")
    return Response(buf.getvalue(), media_type="image/png")


####  /health endpoint
@app.function()
@modal.fastapi_endpoint(method="GET")
def health():
    return {"ok": True}
