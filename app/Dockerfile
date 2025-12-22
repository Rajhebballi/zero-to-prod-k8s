# 1️⃣ Build stage (fat image)
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src src
COPY tests tests

RUN pytest


# 2️⃣ Runtime stage (skinny image)
FROM python:3.11-slim

# install curl FOR HEALTHCHECK (IMPORTANT)
RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Non-root user (security)
RUN useradd -u 10001 appuser
USER appuser

COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin
COPY src src

EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
  CMD curl --fail http://localhost:8080/health || exit 1

CMD ["python", "src/app.py"]
