Coderr – Freelancer-App (Django + DRF)
=====================================

Beschreibung
------------
Coderr ist eine Freelancer-Plattform, entwickelt mit Django und Django REST Framework (DRF).
Nutzer können sich als Kunde oder Anbieter registrieren, Projekte anlegen, Angebote erstellen und Bewertungen austauschen.

Features
--------
- REST-API mit Django REST Framework
- Authentifizierung für Kunden und Freelancer
- Gast-Login („customer“ & „business“) direkt nach Migration verfügbar
- CRUD-Operationen für:
  - Projekte
  - Angebote
  - Reviews
- Berechtigungen: nur der Owner kann eigene Objekte ändern oder löschen
- Automatisch angelegte Gast-Accounts für schnelles Testing

Technologien & Voraussetzungen
------------------------------
- Python 3.9 oder neuer
- Django 4.x
- Django REST Framework
- SQLite (Standard) oder Postgres/MySQL
- pip, virtualenv (empfohlen)

Installation & Setup
--------------------
1. Repository klonen
   git clone <REPO-URL>
   cd coderr-backend

2. Virtual Environment anlegen & aktivieren
   python -m venv env
   source env/bin/activate    # macOS/Linux
   env\Scripts\activate     # Windows

3. Abhängigkeiten installieren
   pip install -r requirements.txt

4. Umgebungsvariablen einrichten
   Lege eine .env-Datei an mit:
     SECRET_KEY=dein_geheimer_schluessel
     DEBUG=True
     DATABASE_URL=sqlite:///db.sqlite3

5. Datenbank-Migrationen durchführen
   python manage.py makemigrations
   python manage.py migrate

   Nach migrate werden zwei Gast-Accounts angelegt:
     - Benutzername: customer  (als Gast-Kunde)
     - Benutzername: business  (als Gast-Freelancer)

Server starten
--------------
python manage.py runserver

Die API ist dann erreichbar unter:
http://127.0.0.1:8000/api/

Wichtige API-Endpunkte
-----------------------
- Authentifizierung:
  - POST /api/auth/login/
  - POST /api/auth/register/
- Projekte:
  - GET  /api/projects/
  - POST /api/projects/
  - GET  /api/projects/{id}/
  - PATCH/DELETE /api/projects/{id}/
- Angebote:
  - GET  /api/offers/
  - POST /api/offers/
- Bewertungen (Reviews):
  - GET  /api/reviews/    (liefert nur eigene Reviews)
  - POST /api/reviews/

Testing
-------
- Unit- und Integrationstests ausführen:
  python manage.py test

Deployment (Kurzüberblick)
--------------------------
- Empfohlen: Gunicorn + NGINX
- Umgebungsvariablen sicher über Server-Konfiguration oder CI/CD bereitstellen
- Optional: Docker-Compose für lokale Produktivumgebung

Beitragen
---------
1. Fork erstellen
2. Neuen Branch anlegen (git checkout -b feature/meine-idee)
3. Änderungen committen (git commit -m "Add …")
4. Push zum Branch (git push origin feature/meine-idee)
5. Pull Request öffnen

Lizenz
------
Dieses Projekt steht unter der MIT-Lizenz.
Bitte siehe die Datei LICENSE für Details.
