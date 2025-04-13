FROM python:3.12-slim AS base

RUN apt-get update && apt-get install -y curl && \
    curl -LO https://github.com/astral-sh/uv/releases/download/0.1.23/uv-x86_64-unknown-linux-gnu.tar.gz && \
    tar xzf uv-x86_64-unknown-linux-gnu.tar.gz && \
    mv uv-x86_64-unknown-linux-gnu/uv /usr/local/bin/ && \
    chmod +x /usr/local/bin/uv && \
    rm -r uv-x86_64-unknown-linux-gnu uv-x86_64-unknown-linux-gnu.tar.gz && \
    apt-get purge -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync

COPY . .

CMD ["python", "-m", "main"]