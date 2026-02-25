FROM python:3.12-slim AS base

# System dependencies: git for PR creation, curl for gh CLI, gcc for hdbscan build
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
    -o /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
    > /etc/apt/sources.list.d/github-cli.list \
    && apt-get update && apt-get install -y --no-install-recommends gh \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download sentence-transformer models so they're baked into the image
# (avoids ~500MB download on every run)
RUN python -c "\
from sentence_transformers import SentenceTransformer, CrossEncoder; \
SentenceTransformer('intfloat/multilingual-e5-small'); \
CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')"

# Install boto3 for S3/SES and python-dotenv (used by src/__init__.py)
RUN pip install --no-cache-dir boto3 python-dotenv

# Copy application code
COPY src/ src/
COPY leaders_sources.csv .
COPY opinion_filters.csv .
COPY scripts/ scripts/

ENTRYPOINT ["python", "-m", "scripts.run_pipeline"]
