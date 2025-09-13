### STAGE 1: base image
ARG DOCKER_REGISTRY=ghcr.io
ARG VERSION=0.6.11
FROM $DOCKER_REGISTRY/kagent-dev/kagent/kagent-adk:$VERSION

USER root
WORKDIR /app

COPY  agent/ agent/
COPY  pyproject.toml pyproject.toml
COPY  README.md README.md
COPY  uv.lock uv.lock

RUN uv sync --locked --refresh


CMD ["agent"]