FROM python:3.12-slim AS base

FROM base AS builder

RUN apt-get update && apt-get install -y curl && \
    curl -LO https://github.com/astral-sh/uv/releases/download/0.4.18/uv-x86_64-unknown-linux-gnu.tar.gz && \
    tar xzf uv-x86_64-unknown-linux-gnu.tar.gz && \
    mv uv-x86_64-unknown-linux-gnu/uv /usr/local/bin/ && \
    chmod +x /usr/local/bin/uv && \
    rm -r uv-x86_64-unknown-linux-gnu uv-x86_64-unknown-linux-gnu.tar.gz && \
    apt-get purge -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN uv pip install . --system --no-cache-dir

FROM base AS final

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

CMD ["python", "-m", "main"]
