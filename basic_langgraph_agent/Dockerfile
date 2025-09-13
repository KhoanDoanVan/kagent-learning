FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
  build-essential \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy project files (excluding packages directory)
COPY agent/ agent/
COPY pyproject.toml pyproject.toml
COPY README.md README.md
COPY uv.lock uv.lock

# Install dependencies
RUN uv sync --locked --no-dev

ENV PYTHONPATH=/app
ENV PORT=8080

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

CMD ["uv", "run", "python", "agent/cli.py"]