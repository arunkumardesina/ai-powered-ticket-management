# AI-Powered Ticket Management

Django REST Framework authorization foundation for the customer support platform. The existing Django project is retained at the repository root in `aiticket/`.

## Current scope
- Role-aware custom user model: CUSTOMER, AGENT, ADMIN.
- Public registration always creates a CUSTOMER; caller cannot assign privileged roles.
- JWT login, token refresh, authenticated profile endpoint and refresh-token blacklist logout.
- DRF authentication required by default and reusable role permission classes.
- Environment-based secret key and tests for registration, login, profile and logout.

## Setup (run from repository root, where manage.py exists)
```cmd
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
copy .env.example .env
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Put the generated key in `.env` as `DJANGO_SECRET_KEY=...`, then run:
```cmd
python manage.py makemigrations accounts
python manage.py migrate
python manage.py test accounts
python manage.py createsuperuser
python manage.py runserver
```

## Auth API
Base: `http://127.0.0.1:8000/api/auth/`

| Method | Endpoint | Access | Purpose |
|---|---|---|---|
| POST | `register/` | Public | Create customer account |
| POST | `login/` | Public | Obtain access and refresh JWT |
| POST | `token/refresh/` | Refresh token | Refresh access token |
| POST | `logout/` | Authenticated | Blacklist current user's refresh token |
| GET | `me/` | Authenticated | Get current user and role |

Login accepts `username` and `password`. Registration accepts username, email, password and password_confirm. It never accepts a role. Agent/admin accounts must be provisioned by trusted staff.

SQLite remains the default so a fresh clone is runnable. MySQL can be enabled by installing compatible `mysqlclient` and setting DB_ENGINE plus DB_* variables in the local .env.

## Deployment checklist
Before production: DEBUG=False, strong unique secret, correct ALLOWED_HOSTS, HTTPS, secure cookies, CORS/CSRF restrictions, login and registration throttling, verified email, password reset, object-level authorization and monitoring. Google OAuth, OpenAI, React frontend and WebSocket chat are not implemented in this authorization milestone.
