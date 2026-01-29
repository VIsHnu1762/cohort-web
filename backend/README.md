# Cohort Web Application - Backend

Backend API for the Cohort Web Application built with Django REST Framework.

## Tech Stack

- **Django 4.2.7** - Web framework
- **Django REST Framework 3.14.0** - API framework
- **PostgreSQL** - Database
- **JWT Authentication** - Token-based auth
- **Swagger/OpenAPI** - API documentation

## Project Structure

```
backend/
├── config/              # Django project settings
│   ├── settings.py     # Main settings
│   ├── urls.py         # URL routing
│   ├── wsgi.py         # WSGI config
│   └── asgi.py         # ASGI config
├── apps/                # Django applications
│   ├── clt/            # Creative Learning Track
│   ├── sri/            # Social Responsibility Initiative
│   ├── cfc/            # Career, Future & Competency
│   ├── iipc/           # Industry Interaction & Professional Connect
│   └── scd/            # Skill & Career Development
├── media/              # User uploaded files
├── static/             # Static files
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

## Setup Instructions

### 1. Prerequisites

- Python 3.10+
- PostgreSQL 15+
- pip (Python package manager)

### 2. Database Setup

Create PostgreSQL database:

```sql
CREATE DATABASE cohort_db;
CREATE USER your_db_user WITH PASSWORD 'your_password';
ALTER ROLE your_db_user SET client_encoding TO 'utf8';
ALTER ROLE your_db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_db_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE cohort_db TO your_db_user;
```

### 3. Environment Setup

Create `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Update the `.env` file with your configuration:

```
DB_NAME=cohort_db
DB_USER=your_db_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-secret-key-here
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Server will start at: `http://127.0.0.1:8000/`

## API Documentation

Once the server is running, access:

- **Swagger UI**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/redoc/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## API Endpoints

### CLT (Creative Learning Track)
- `POST /api/clt/submissions/` - Create course submission
- `GET /api/clt/submissions/` - List all submissions
- `GET /api/clt/submissions/{id}/` - Get submission details
- `PUT /api/clt/submissions/{id}/` - Update submission
- `DELETE /api/clt/submissions/{id}/` - Delete submission

### SRI (Social Responsibility Initiative)
- `POST /api/sri/activities/` - Create social activity
- `GET /api/sri/activities/` - List all activities
- Similar CRUD operations...

### CFC (Career, Future & Competency)
- Career-related endpoints (to be implemented)

### IIPC (Industry Interaction)
- LinkedIn verification endpoints (to be implemented)

### SCD (Skill & Career Development)
- Coding platform verification endpoints (to be implemented)

## Development Workflow

1. Always work in the `sriram_backend` branch
2. Never push to `main` branch
3. Test APIs using Swagger UI or Postman
4. Follow Django best practices
5. Write docstrings for all functions
6. Add proper validation and error handling

## Testing

Run tests:

```bash
python manage.py test
```

## Production Deployment

For production:

1. Set `DEBUG=False` in `.env`
2. Configure proper `ALLOWED_HOSTS`
3. Use Gunicorn: `gunicorn config.wsgi:application`
4. Set up Nginx as reverse proxy
5. Use environment-specific database
6. Enable HTTPS/SSL

## Notes

- Authentication system is handled by another team member
- Frontend runs on ports 5173/5174
- Backend API runs on port 8000
- CORS is configured for local development

## Team Member Responsibilities

- **Auth Team**: JWT authentication, user management
- **Your Team**: CLT, SRI, CFC, IIPC, SCD modules

## Support

For issues or questions, contact the development team.
