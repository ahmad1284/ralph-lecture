FROM python:3.11-slim

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    espeak-ng \
    libespeak-ng1 \
    libcairo2-dev \
    libpango1.0-dev \
    pkg-config \
    python3-dev \
    build-essential \
    git \
    nodejs \
    npm \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Remotion dependencies
COPY remotion-src/package.json remotion-src/package-lock.json remotion-src/
RUN cd remotion-src && npm ci

COPY . .

ENV ANTHROPIC_API_KEY=""

# Usage:
#   docker run -e ANTHROPIC_API_KEY=sk-... -v $(pwd)/output:/app/output ralph-lecture "how to use sed"
#   docker run -v $(pwd)/output:/app/output ralph-lecture --from-script output/how-to-use-sed
ENTRYPOINT ["python", "main.py"]
