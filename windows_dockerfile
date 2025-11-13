FROM python:3.12-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# System-Pakete installieren, die Python-Module wie cryptography, bcrypt etc. brauchen
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libffi-dev libssl-dev libjpeg-dev zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*

# Erst requirements.txt kopieren und Abhängigkeiten installieren
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Restlichen Code kopieren
COPY . .

# Standard-Kommando
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
