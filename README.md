# Coderr – Freelancer App (Django + DRF)

## 📝 Description
Coderr ist eine Freelancer-Plattform, die mit **Django** und **Django REST Framework (DRF)** gebaut wurde.  
Benutzer können sich als Kunde oder Freelancer registrieren, Projekte erstellen, Angebote abgeben und Bewertungen austauschen.

---

## 🚀 Features
- ✅ REST API mit Django REST Framework  
- 🔐 Authentifizierung für Kunden und Freelancer  
- 👥 Gast-Login (`"customer"` & `"freelancer"`) sofort nach Migration verfügbar  
- ✍️ CRUD-Operationen für:
  - Projekte
  - Angebote
  - Bewertungen
- 🔒 Berechtigungen: Nur Eigentümer können ihre Objekte bearbeiten oder löschen  
- 🧪 Automatisch generierte Gast-Accounts zum Testen

---

## 🛠️ Technologien & Voraussetzungen
- Python **3.9 oder höher**  
- Django **4.x**  
- Django REST Framework  
- **SQLite** (Standard) oder **PostgreSQL/MySQL**  
- `pip`, `virtualenv` (empfohlen)

---

## ⚙️ Installation & Setup

```bash
# 1. Repository klonen
git clone <REPO-URL>
cd coderr-backend

# 2. Virtuelle Umgebung erstellen & aktivieren
python -m venv env
source env/bin/activate    # macOS/Linux
env\Scripts\activate       # Windows

# 3. Abhängigkeiten installieren
pip install -r requirements.txt

# 4. Migrationen ausführen
python manage.py makemigrations
python manage.py migrate
```

> Nach der Migration werden zwei Gast-Accounts erstellt:
> - Benutzername: `kevin`  (Gastkunde)  
> - Benutzername: `andrey` (Gastfreelancer)

---

## ▶️ Server starten

```bash
python manage.py runserver
```

Die API ist dann erreichbar unter:  
👉 http://127.0.0.1:8000/api/

---

## 📡 Wichtige API-Endpunkte

### 🔐 Authentifizierung
```http
POST /api/auth/login/
POST /api/auth/register/
```

### 📁 Projekte
```http
GET    /api/projects/
POST   /api/projects/
GET    /api/projects/{id}/
PATCH  /api/projects/{id}/
DELETE /api/projects/{id}/
```

### 💼 Angebote
```http
GET  /api/offers/
POST /api/offers/
```

### 🌟 Bewertungen
```http
GET  /api/reviews/        # zeigt nur deine eigenen Bewertungen
POST /api/reviews/
```

---

## 🚢 Deployment (Überblick)
- Empfohlen: **Gunicorn + NGINX**
- Umgebungsvariablen sicher über Server-Konfiguration oder CI/CD bereitstellen
- Optional: **Docker Compose** für produktionsähnliches lokales Setup

---

## 🤝 Mitwirken
1. Repository forken  
2. Neuen Branch erstellen:
   ```bash
   git checkout -b feature/meine-idee
   ```
3. Änderungen committen:
   ```bash
   git commit -m "Add ..."
   ```
4. Branch pushen:
   ```bash
   git push origin feature/meine-idee
   ```
5. Pull Request öffnen

---

## 📄 Lizenz
Dieses Projekt steht unter der **MIT License**.  
Siehe die Datei `LICENSE` für Details.
