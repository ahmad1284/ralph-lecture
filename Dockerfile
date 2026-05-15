FROM python:3.11-slim

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    espeak-ng \
    libespeak-ng1 \
    git \
    nodejs \
    npm \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python package (deps resolved from pyproject.toml)
COPY pyproject.toml README.md ./
COPY src/ src/
RUN pip install --no-cache-dir .

# Remotion dependencies
COPY remotion-src/package.json remotion-src/package-lock.json remotion-src/
RUN cd remotion-src && npm ci

# Copy the rest (examples, etc.)
COPY . .

ENV ANTHROPIC_API_KEY=""

# docker run -e ANTHROPIC_API_KEY=sk-... -v $(pwd)/output:/app/output prompt2video "how to use grep"
# docker run -v $(pwd)/output:/app/output prompt2video --from-script examples/how-to-use-sed
ENTRYPOINT ["prompt2video"]
