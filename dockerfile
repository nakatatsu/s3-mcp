FROM python:3.12-slim AS base

FROM base AS uv-installer
RUN apt-get update && apt-get install -y curl && \
    mkdir -p /tmp/uv && cd /tmp/uv && \
    curl -L https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-unknown-linux-gnu.tar.gz | tar xz && \
    install -m 755 uv /usr/local/bin/uv && \
    cd / && rm -rf /tmp/uv && \
    apt-get purge -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*

FROM base AS builder
WORKDIR /app
COPY --from=uv-installer /usr/local/bin/uv /usr/local/bin/uv
COPY pyproject.toml uv.lock ./
RUN uv install --system --no-cache-dir

FROM base AS final
WORKDIR /app
COPY --from=builder /usr/local /usr/local
COPY . .

CMD ["python", "-m", "main"]
