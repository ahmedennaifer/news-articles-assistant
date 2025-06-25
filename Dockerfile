FROM python:3.10-slim as builder

WORKDIR /app

COPY pyproject.toml .

RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    pip install uv && \
    uv venv .virtualenv && \
    . .virtualenv/bin/activate && \
    uv pip install -e . && \
    apt-get purge -y git && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*



FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /app/.virtualenv /app/.virtualenv

COPY . .

RUN pip install uv

ENV PATH="/app/.virtualenv/bin:$PATH"
ENV GROQ_KEY=${GROQ_KEY}
ENV HF_KEY=${HF_KEY}
ENV POSTGRES_USER=${POSTGRES_USER}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ENV POSTGRES_DB=${POSTGRES_DB}

EXPOSE 5432
EXPOSE 8000

# CMD ["/bin/bash", "-c","PYTHONPATH=/app python src/assistant/evaluators/mrr_evaluator.py"]
# CMD ["/bin/bash", "-c","PYTHONPATH=/app python src/etl/ingest.py"]
# CMD ["/bin/bash", "-c","PYTHONPATH=/app python src/assistant/pipelines/index_pipeline.py"]
# CMD ["/bin/bash", "-c","PYTHONPATH=/app python src/main.py"]
CMD ["/bin/bash", "-c", "uvicorn src.backend.routes.main:app --host 0.0.0.0 --port 8000 --reload"]


