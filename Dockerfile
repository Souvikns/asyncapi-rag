FROM python:3.11
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app

COPY . /app

RUN uv sync --locked

EXPOSE 8000

CMD ["uv", "run", "fastapi", "run", "server.py"]

