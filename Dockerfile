FROM postgres:17.11-alpine3.24 AS database

# Start PostgreSQL directly as its service user; no root-switching helper is needed.
RUN apk upgrade --no-cache && rm /usr/local/bin/gosu
USER postgres

FROM ghcr.io/astral-sh/uv:0.13.6 AS uv-bin

FROM python:3.12.15-alpine3.24 AS app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1 \
    PATH="/app/.venv/bin:${PATH}"

WORKDIR /app

COPY --from=uv-bin /uv /uvx /bin/

# uv installs the application; the base image's pip is not needed at runtime.
RUN /usr/local/bin/python -m pip uninstall --yes pip

RUN addgroup -g 10001 portfolio \
    && adduser -D -u 10001 -G portfolio portfolio \
    && mkdir -p /app/artifacts \
    && chown -R portfolio:portfolio /app

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --locked --no-dev --no-install-project

COPY src ./src
RUN uv sync --locked --no-dev --no-editable \
    && chown -R portfolio:portfolio /app

USER portfolio
EXPOSE 8000

HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=12 \
    CMD ["python", "-c", "from urllib.request import urlopen; urlopen('http://127.0.0.1:8000/health', timeout=2)"]

CMD ["python", "-m", "uvicorn", "demo_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
