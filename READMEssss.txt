Coderr – Freelancer App (Django + DRF)
======================================

Description
-----------
Coderr is a freelancer platform built with Django and Django REST Framework (DRF).
Users can register as customers or freelancers, create projects, make offers, and exchange reviews.

Features
--------
- REST API with Django REST Framework
- Authentication for customers and freelancers
- Guest login ("customer" & "business") available immediately after migration
- CRUD operations for:
  - Projects
  - Offers
  - Reviews
- Permissions: only owners can modify or delete their own objects
- Auto-generated guest accounts for easy testing

Technologies & Requirements
---------------------------
- Python 3.9 or higher
- Django 4.x
- Django REST Framework
- SQLite (default) or PostgreSQL/MySQL
- pip, virtualenv (recommended)

Installation & Setup
--------------------
1. Clone the repository
   git clone <REPO-URL>
   cd coderr-backend

2. Create & activate a virtual environment
   python -m venv env
   source env/bin/activate    # macOS/Linux
   env\Scripts\activate     # Windows

3. Install dependencies
   pip install -r requirements.txt

4. Run database migrations
   python manage.py makemigrations
   python manage.py migrate

   After migrate, two guest accounts are created:
     - Username: kevin  (guest as a customer)
     - Username: andrey  (guest as a freelancer)

Starting the Server
-------------------
python manage.py runserver

The API will be available at:
http://127.0.0.1:8000/api/

Key API Endpoints
-----------------
- Authentication:
  - POST /api/auth/login/
  - POST /api/auth/register/
- Projects:
  - GET  /api/projects/
  - POST /api/projects/
  - GET  /api/projects/{id}/
  - PATCH/DELETE /api/projects/{id}/
- Offers:
  - GET  /api/offers/
  - POST /api/offers/
- Reviews:
  - GET  /api/reviews/    (returns only your own reviews)
  - POST /api/reviews/


Deployment (Overview)
---------------------
- Recommended: Gunicorn + NGINX
- Provide environment variables securely via server config or CI/CD
- Optional: Docker Compose for local production-like setup

Contributing
------------
1. Fork the repository
2. Create a new branch (git checkout -b feature/my-idea)
3. Commit your changes (git commit -m "Add ...")
4. Push to your branch (git push origin feature/my-idea)
5. Open a pull request

License
-------
This project is licensed under the MIT License.
See the LICENSE file for details.
