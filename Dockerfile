FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    HF_HUB_DISABLE_SYMLINKS_WARNING=1 \
    # pass Hugging Face token at run-time if you need private models
    HF_TOKEN=${HF_TOKEN:-""}

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc git curl ca-certificates libgl1 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY app /app
WORKDIR /app

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]