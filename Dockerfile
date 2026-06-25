# ─── Raspberry Pi ARM64-kompatibelt image ───────────────────────────────────
FROM python:3.11-slim-bookworm

LABEL maintainer="Claude Pi Portal"
LABEL description="Claude AI + Python scripts portal til Raspberry Pi"

# Systemafhængigheder
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Arbejdsmappe
WORKDIR /app

# Python-pakker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App-kode
COPY app/ ./app/

# Scripts-mappe (monteres som volume)
RUN mkdir -p /data/scripts /data/uploads /data/logs

# Port til web-GUI
EXPOSE 5000

# Miljøvariabler (overskrives i docker-compose)
ENV FLASK_APP=app/main.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
