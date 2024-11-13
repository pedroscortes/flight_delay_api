# syntax=docker/dockerfile:1.2
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements-dev.txt requirements-test.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY challenge/ ./challenge/
COPY data/ ./data/

ENV PORT=8080
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8080"]