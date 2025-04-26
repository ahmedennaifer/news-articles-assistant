FROM python:3.10

WORKDIR /app 

COPY . .

ENV GROQ_KEY=${GROQ_KEY}
ENV HF_KEY=${HF_KEY}

ENV POSTGRES_USER=${POSTGRES_USER}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ENV POSTGRES_DB=${POSTGRES_DB}

EXPOSE 5432

RUN apt-get update && \
  python -m ensurepip --upgrade && \
  pip install uv && \
  uv venv .virtualenv  

RUN . .virtualenv/bin/activate && \
  uv pip install -r requirements.txt  

CMD ["/bin/bash", "-c","PYTHONPATH=/app  uv run src/api/etl/ingest.py &&  PYTHONPATH=/app uv run src/main.py "] 




