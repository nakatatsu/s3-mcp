FROM python:3.12-slim AS base

FROM base AS uv-installer
RUN apt-get update && apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    apt-get purge -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*

FROM base AS builder
WORKDIR /app
COPY --from=uv-installer /root/.cargo/bin/uv /usr/local/bin/uv
COPY pyproject.toml uv.lock ./
RUN uv install --system --no-cache-dir

FROM base AS final
WORKDIR /app
COPY --from=builder /usr/local /usr/local
COPY . .

CMD ["python", "-m", "main"]
