FROM python:3.13  

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN mkdir /backend
WORKDIR /backend
COPY ./uv.lock /backend/uv.lock
COPY ./pyproject.toml /backend/pyproject.toml

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

RUN uv sync --locked
