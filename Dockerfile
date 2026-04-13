FROM python:3.12-slim

# System dependencies: git for cloning/pushing, gcc for hdbscan build
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir boto3 python-dotenv

# Playwright needs its driver + system deps for CDP connections to Browserbase
RUN playwright install --with-deps chromium

# Pre-download sentence-transformer models (~500MB, avoids download per run)
RUN python -c "\
from sentence_transformers import SentenceTransformer, CrossEncoder; \
SentenceTransformer('intfloat/multilingual-e5-small'); \
CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')"

# Only the entrypoint script — everything else comes from the clone at runtime
COPY scripts/__init__.py scripts/__init__.py
COPY scripts/run_pipeline.py scripts/run_pipeline.py

ENTRYPOINT ["python", "scripts/run_pipeline.py"]
