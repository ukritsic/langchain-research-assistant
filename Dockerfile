# Dockerfile for Multi-Document Research Assistant
FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Faster, quieter pip; deterministic locale & HF cache
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/app/.cache/huggingface

WORKDIR /app

# Install Python deps first for cache efficiency
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy project
COPY . /app

# Ensure runtime dirs exist (usually mounted as volumes)
RUN mkdir -p /app/docs

# Default entrypoint
ENTRYPOINT ["python", "main.py"]
CMD ["-h"]