C:\Python310\cohort_webapp\cohort>curl -X POST https://wholesome-cat-production.up.railway.app/api/setup-database/ -d "setup_key=cohort_setup_2024"
{"admin_created": false, "students_created": 0, "students_updated": 0, "errors": ["CSV not found. Tried: ['/app/apps/../../dummy users - Sheet1.csv', '/app/apps/../../../dummy users - Sheet1.csv', '/app/dummy users - Sheet1.csv']"], "admin_updated": true}
C:\Python310\cohort_webapp\cohort># Railway Deployment Guide - Cohort Web Application

This guide walks you through deploying the Cohort Web Application on Railway.app with PostgreSQL database.

## Prerequisites

- GitHub account with your repository
- Railway account (sign up at https://railway.app)
- Code pushed to GitHub main branch

---

## Part 1: Deploy Backend (Django + PostgreSQL)

### Step 1: Create Railway Project

1. Go to https://railway.app and click **"Start a New Project"**
2. Select **"Deploy from GitHub repo"**
3. Authorize Railway to access your GitHub account
4. Select your `cohort` repository
5. Railway will detect it as a Python project

### Step 2: Add PostgreSQL Database

1. In your Railway project dashboard, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway will automatically provision a PostgreSQL database
4. The database will be connected to your backend service

### Step 3: Configure Backend Environment Variables

1. Click on your **backend service** (Django app)
2. Go to **"Variables"** tab
3. Add the following environment variables:

```bash
# Django Settings
DJANGO_SETTINGS_MODULE=config.settings
SECRET_KEY=your-super-secret-key-here-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=.railway.app,.up.railway.app
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.up.railway.app

# Database (Railway auto-provides DATABASE_URL)
# DATABASE_URL is automatically set by Railway PostgreSQL

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Email (Optional - for notifications)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
```

**Important Notes:**
- `DATABASE_URL` is automatically provided by Railway when you add PostgreSQL
- Generate a strong `SECRET_KEY` using: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- Update `CORS_ALLOWED_ORIGINS` after deploying frontend

### Step 4: Configure Build Settings

1. Go to **"Settings"** tab in your backend service
2. Set **Root Directory**: `backend`
3. Set **Build Command**: 
   ```bash
   pip install -r requirements.txt
   ```
4. Set **Start Command**:
   ```bash
   python manage.py migrate && python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
   ```

### Step 5: Add Railway Configuration Files

Create `railway.json` in your `backend/` directory:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Step 6: Update Django Settings for Railway

Ensure your `backend/config/settings.py` has:

```python
import dj_database_url
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key-for-development')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# CORS Settings
CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:5173,http://localhost:3000'
).split(',')

# Database Configuration
if os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Security Settings for Production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
```

### Step 7: Deploy Backend

1. Push your changes to GitHub:
   ```bash
   git add .
   git commit -m "Configure for Railway deployment"
   git push origin main
   ```

2. Railway will automatically detect the push and start deploying

3. Monitor deployment in the **"Deployments"** tab

4. Once deployed, click **"Settings"** → **"Networking"** → **"Generate Domain"** to get your backend URL

---

## Part 2: Deploy Frontend (React + Vite)

### Step 1: Add Frontend Service

1. In your Railway project, click **"+ New"**
2. Select **"GitHub Repo"** → Select your repository again
3. Railway will create a new service for the frontend

### Step 2: Configure Frontend Environment Variables

1. Click on your **frontend service**
2. Go to **"Variables"** tab
3. Add the following:

```bash
# API Configuration
VITE_API_URL=https://your-backend-domain.up.railway.app
NODE_ENV=production
```

**Important:** Replace `your-backend-domain` with the actual domain from your backend service

### Step 3: Configure Frontend Build Settings

1. Go to **"Settings"** tab
2. Set **Root Directory**: `.` (leave empty or set to root)
3. Set **Build Command**:
   ```bash
   npm install && npm run build
   ```
4. Set **Start Command**:
   ```bash
   npm run preview -- --host 0.0.0.0 --port $PORT
   ```

### Step 4: Add Frontend Railway Configuration

Create `railway.json` in your project root:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "npm install && npm run build"
  },
  "deploy": {
    "startCommand": "npm run preview -- --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Step 5: Update Vite Configuration

Update `vite.config.js`:

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173
  },
  preview: {
    host: '0.0.0.0',
    port: process.env.PORT || 4173
  },
  build: {
    outDir: 'dist',
    sourcemap: false
  }
})
```

### Step 6: Update API URL in Frontend

Update your API service file (e.g., `src/services/api.js`):

```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default API_URL;
```

### Step 7: Deploy Frontend

1. Push changes to GitHub:
   ```bash
   git add .
   git commit -m "Configure frontend for Railway deployment"
   git push origin main
   ```

2. Railway will automatically deploy the frontend

3. Once deployed, generate a domain for the frontend:
   - Go to **"Settings"** → **"Networking"** → **"Generate Domain"**

---

## Part 3: Connect Backend and Frontend

### Step 1: Update Backend CORS Settings

1. Go to backend service → **"Variables"**
2. Update `CORS_ALLOWED_ORIGINS` with your frontend domain:
   ```
   CORS_ALLOWED_ORIGINS=https://your-frontend-domain.up.railway.app
   ```

3. Update `ALLOWED_HOSTS`:
   ```
   ALLOWED_HOSTS=your-backend-domain.up.railway.app,.railway.app
   ```

### Step 2: Redeploy Backend

Railway will automatically redeploy when you update environment variables.

### Step 3: Test the Connection

1. Open your frontend URL in a browser
2. Try logging in with test credentials
3. Check browser console for any CORS errors
4. Verify API calls are reaching the backend

---

## Part 4: Initialize Database and Create Superuser

### Step 1: Access Backend Shell

1. In Railway dashboard, click on your backend service
2. Go to **"Settings"** tab
3. Scroll down to **"Service"** section
4. Click on **"Connect"** or use Railway CLI

### Step 2: Run Database Migrations

Using Railway CLI:
```bash
railway run python manage.py migrate
```

Or connect via web console and run:
```bash
python manage.py migrate
```

### Step 3: Create Superuser

```bash
railway run python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### Step 4: Load Initial Data (Optional)

If you have fixture data:
```bash
railway run python manage.py loaddata initial_data.json
```

---

## Part 5: Post-Deployment Configuration

### 1. Custom Domains (Optional)

#### Backend Domain:
1. Go to backend service → **"Settings"** → **"Networking"**
2. Click **"Custom Domain"**
3. Add your domain (e.g., `api.yoursite.com`)
4. Update your DNS records with the provided CNAME

#### Frontend Domain:
1. Go to frontend service → **"Settings"** → **"Networking"**
2. Click **"Custom Domain"**
3. Add your domain (e.g., `app.yoursite.com`)
4. Update your DNS records

### 2. Environment-Specific Settings

Create `.env.production` in frontend:
```bash
VITE_API_URL=https://api.yoursite.com
```

### 3. Monitoring and Logs

- View logs in Railway dashboard → **"Deployments"** → Click on deployment → **"View Logs"**
- Set up monitoring alerts in **"Settings"** → **"Observability"**

### 4. Database Backups

1. Go to PostgreSQL service → **"Settings"**
2. Enable automatic backups
3. Configure backup schedule

---

## Troubleshooting

### Issue: Backend Won't Start

**Solution:**
- Check environment variables are set correctly
- Verify `DATABASE_URL` is present
- Check logs for specific errors
- Ensure `requirements.txt` includes all dependencies

### Issue: Static Files Not Loading

**Solution:**
```bash
# In backend service, run:
railway run python manage.py collectstatic --noinput
```

Update `settings.py`:
```python
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

Add to `requirements.txt`:
```
whitenoise==6.6.0
```

### Issue: CORS Errors

**Solution:**
- Verify `CORS_ALLOWED_ORIGINS` includes your frontend domain
- Check `ALLOWED_HOSTS` includes backend domain
- Ensure frontend is using correct API URL

### Issue: Database Connection Failed

**Solution:**
- Verify PostgreSQL service is running
- Check `DATABASE_URL` environment variable
- Ensure database migrations ran successfully

### Issue: 502 Bad Gateway

**Solution:**
- Check start command is correct
- Verify port binding: `0.0.0.0:$PORT`
- Check service logs for startup errors

---

## Railway CLI (Optional)

### Install Railway CLI:
```bash
npm i -g @railway/cli
```

### Login:
```bash
railway login
```

### Link Project:
```bash
railway link
```

### View Logs:
```bash
railway logs
```

### Run Commands:
```bash
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

---

## Cost Optimization

1. **Use Hobby Plan**: $5/month for both services
2. **Set Sleep Policy**: Configure services to sleep after inactivity
3. **Optimize Database**: Use connection pooling
4. **Monitor Usage**: Check Railway dashboard for resource usage

---

## Security Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` generated
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] `CORS_ALLOWED_ORIGINS` restricted to your domain
- [ ] SSL/HTTPS enabled (automatic with Railway)
- [ ] Database credentials secured (automatic with Railway)
- [ ] Environment variables not committed to Git
- [ ] Static files served securely
- [ ] Admin panel secured with strong password

---

## Maintenance

### Regular Updates:
```bash
# Update dependencies
pip install --upgrade -r requirements.txt
npm update

# Run migrations
railway run python manage.py migrate

# Collect static files
railway run python manage.py collectstatic --noinput
```

### Monitoring:
- Check Railway dashboard regularly
- Monitor error rates
- Review database performance
- Check disk usage

---

## Support

- Railway Documentation: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Railway Status: https://status.railway.app

---

## Summary

Your application is now deployed on Railway with:

✅ Backend (Django) with PostgreSQL database
✅ Frontend (React + Vite) 
✅ Automatic deployments from GitHub
✅ SSL/HTTPS enabled
✅ Environment variables configured
✅ Database migrations applied

**Your URLs:**
- Backend API: `https://your-backend.up.railway.app`
- Frontend App: `https://your-frontend.up.railway.app`
- Admin Panel: `https://your-backend.up.railway.app/admin`

**Default Test Credentials:**
- Email: test_student@cohort.com
- Username: test_student
- Password: test_password_123

(Create your own admin/superuser for production)
