# Coderr – Freelancer App (Django + DRF)

## 📝 Description
Coderr is a freelancer platform built with **Django** and **Django REST Framework (DRF)**.  
Users can register as customers or freelancers, create projects, submit offers, and exchange reviews.

---

## 🚀 Features
- ✅ REST API using Django REST Framework  
- 🔐 Authentication for both customers and freelancers  
- 👥 Guest login (`"customer"` & `"freelancer"`) available after migrations  
- ✍️ Full CRUD functionality for:
  - Projects
  - Offers
  - Reviews
- 🔒 Permissions: only owners can edit or delete their own objects  
- 🧪 Auto-generated guest accounts for testing

---

## 🛠️ Technologies & Requirements
- Python **3.9 or higher**  
- Django **4.x**  
- Django REST Framework  
- **SQLite** (default) or **PostgreSQL/MySQL**  
- `pip`, `virtualenv` (recommended)

---

## ⚙️ Installation & Setup

```bash
# 1. Clone the repository
git clone <REPO-URL>
cd coderr-backend

# 2. Create and activate a virtual environment
python -m venv env
source env/bin/activate    # macOS/Linux
env\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py makemigrations
python manage.py migrate
```

> After migration, two guest accounts will be created:
> - Username: `kevin`  (guest customer)  
> - Username: `andrey` (guest freelancer)

---

## ▶️ Starting the Server

```bash
python manage.py runserver
```

API will be accessible at:  
👉 http://127.0.0.1:8000/api/

---

## 📡 Key API Endpoints

### 🔐 Authentication
```http
POST /api/auth/login/
POST /api/auth/register/
```

### 📁 Projects
```http
GET    /api/projects/
POST   /api/projects/
GET    /api/projects/{id}/
PATCH  /api/projects/{id}/
DELETE /api/projects/{id}/
```

### 💼 Offers
```http
GET  /api/offers/
POST /api/offers/
```

### 🌟 Reviews
```http
GET  /api/reviews/        # returns only your own reviews
POST /api/reviews/
```

---

## 🚢 Deployment (Overview)
- Recommended: **Gunicorn + NGINX**
- Provide environment variables securely via server config or CI/CD
- Optional: **Docker Compose** for local production-like setup

---

## 🤝 Contributing
1. Fork the repository  
2. Create a new branch:
   ```bash
   git checkout -b feature/my-idea
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add ..."
   ```
4. Push to your branch:
   ```bash
   git push origin feature/my-idea
   ```
5. Open a pull request

---

## 📄 License
This project is licensed under the **MIT License**.  
See the `LICENSE` file for more details.
