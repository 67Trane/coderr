FROM python:3.12-slim

# Non-root-User anlegen für mehr Sicherheit
RUN useradd -m appuser

# Arbeitsverzeichnis im Container
WORKDIR /app

# System-Pakete installieren
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*

# requirements zuerst kopieren
COPY requirements.txt .

# Python-Dependencies + Gunicorn installieren
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir gunicorn

# Restlichen Code kopieren
COPY . .

# Rechte auf non-root-User setzen
RUN chown -R appuser:appuser /app

# Ab hier unter non-root laufen
USER appuser

# Port im Container
EXPOSE 8000

# Gunicorn als Application Server starten
# wichtig: core.wsgi:application → based on WSGI_APPLICATION = "core.wsgi.application"
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
