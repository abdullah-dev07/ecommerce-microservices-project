FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY pyproject.toml .
COPY migrations ./migrations

EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -fsS http://localhost:8001/health || exit 1

# Apply pending Aerich migrations, then start the app. `exec` replaces the
# shell so signals (SIGTERM from `docker stop`) reach uvicorn directly.
CMD ["sh", "-c", "aerich upgrade && exec uvicorn app.main:app --host 0.0.0.0 --port 8001"]
