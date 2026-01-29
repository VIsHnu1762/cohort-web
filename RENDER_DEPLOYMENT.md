# 🚀 Render Deployment Guide

## Prerequisites
- ✅ GitHub account
- ✅ Render account (sign up at render.com with GitHub)
- ✅ Code pushed to GitHub repository

---

## 📋 Step 1: Create Test Users (Before Deployment)

Run this locally to test user creation:

```bash
cd backend
python3 create_role_users.py
```

This creates users for all roles:
- **Admin**: admin@cohort.edu / admin123
- **Mentor**: mentor@cohort.edu / mentor123  
- **Student**: student@cohort.edu / student123
- **Floor Wing**: floorwing@cohort.edu / floorwing123

⚠️ **Change these passwords after deployment!**

---

## 🔧 Step 2: Push Code to GitHub

```bash
# Stage all changes
git add .

# Commit
git commit -m "Prepare for Render deployment"

# Push to main branch
git push origin main
```

---

## 🌐 Step 3: Deploy Backend on Render

### 3.1 Create Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository (`cohort`)
4. Configure the service:

**Basic Settings:**
- **Name**: `cohort-backend` (or any name you want)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: `backend`
- **Runtime**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn config.wsgi:application`

### 3.2 Set Environment Variables

Click **"Environment"** and add these variables:

```bash
SECRET_KEY=your-random-secret-key-here-generate-new-one
DEBUG=False
ALLOWED_HOSTS=.onrender.com
PYTHON_VERSION=3.11.0
```

**Generate SECRET_KEY:**
```python
# Run locally:
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3.3 Add PostgreSQL Database

1. In your web service page, scroll to **"Environment"**
2. Render will prompt to create a PostgreSQL database
3. Click **"Create Database"**
4. Or manually: Dashboard → **"New +"** → **"PostgreSQL"**
   - Name: `cohort-db`
   - Database: `cohort`
   - User: (auto-generated)
   - Region: Same as web service

5. **Link database to web service:**
   - Render automatically adds `DATABASE_URL` environment variable
   - Verify it exists in your web service's Environment tab

### 3.4 Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes first time)
3. Watch logs for any errors

Your backend will be at: `https://cohort-backend.onrender.com`

---

## 👥 Step 4: Create Users on Production

After successful deployment:

### Option A: Using Django Admin

1. Create superuser via Render Shell:
   - Go to your web service
   - Click **"Shell"** tab
   - Run:
   ```bash
   python manage.py createsuperuser
   ```

2. Access admin: `https://cohort-backend.onrender.com/admin/`
3. Create users manually

### Option B: Using Script

1. In Render Shell:
```bash
python create_role_users.py
```

---

## 🎨 Step 5: Deploy Frontend on Vercel

### 5.1 Update Frontend API URL

Edit `src/config.js` (or wherever API URL is configured):

```javascript
const API_URL = import.meta.env.PROD 
  ? 'https://cohort-backend.onrender.com/api'
  : 'http://127.0.0.1:8000/api';

export default API_URL;
```

### 5.2 Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy (from project root)
vercel

# For production
vercel --prod
```

Or use Vercel Dashboard:
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Configure:
   - **Framework**: Vite
   - **Root Directory**: `./` (project root)
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

---

## 🔗 Step 6: Update CORS Settings

After frontend deployment, update backend environment variables on Render:

```bash
CORS_ALLOWED_ORIGINS=https://your-frontend-url.vercel.app,http://localhost:5173
```

Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## ✅ Step 7: Test Deployment

1. **Backend Health Check**: 
   - Visit `https://cohort-backend.onrender.com/admin/`
   - Should see Django admin login

2. **API Test**:
   ```bash
   curl https://cohort-backend.onrender.com/api/
   ```

3. **Frontend**: 
   - Visit your Vercel URL
   - Try logging in with test users

---

## 🐛 Troubleshooting

### Build Fails
- Check logs in Render dashboard
- Verify `build.sh` is executable
- Ensure all dependencies in `requirements.txt`

### Database Connection Error
- Verify `DATABASE_URL` environment variable exists
- Check PostgreSQL database is running

### Static Files Not Loading
- Verify `STATIC_ROOT` and `collectstatic` in build.sh
- Check WhiteNoise is in `MIDDLEWARE`

### CORS Errors
- Add frontend URL to `CORS_ALLOWED_ORIGINS`
- Redeploy backend after changing env vars

### Cold Starts (Free Tier)
- Render free tier sleeps after 15 min inactivity
- First request takes 30-60 seconds
- Subsequent requests are fast

---

## 📊 Monitoring

### Render Dashboard
- View logs: Real-time application logs
- Metrics: CPU, memory usage
- Events: Deployment history

### Check Service Health
```bash
# Health check endpoint (create one if needed)
curl https://cohort-backend.onrender.com/health/
```

---

## 💰 Cost

**Free Tier Limitations:**
- ✅ 750 hours/month (enough for 1 service 24/7)
- ✅ PostgreSQL database included
- ❌ Spins down after 15 min inactivity
- ❌ 90-day data retention limit on DB

**Paid Plans:**
- Starter: $7/month (no sleep, better performance)
- PostgreSQL: $7/month for database

---

## 🔐 Security Checklist

- [ ] Changed `SECRET_KEY` to random value
- [ ] Set `DEBUG=False`
- [ ] Changed all default user passwords
- [ ] Restricted `ALLOWED_HOSTS`
- [ ] Updated `CORS_ALLOWED_ORIGINS`
- [ ] Added `.env` to `.gitignore`
- [ ] Enabled HTTPS only (Render does this automatically)

---

## 📝 Important Notes

1. **First Deploy Takes Time**: 5-10 minutes for initial build
2. **Free Tier Sleeps**: Service becomes inactive after 15 min
3. **Database Backups**: Enable in Render dashboard
4. **Domain**: Can add custom domain (paid plan)
5. **Environment Variables**: Never commit secrets to Git

---

## 🆘 Need Help?

- **Render Docs**: https://render.com/docs/deploy-django
- **Django Deployment**: https://docs.djangoproject.com/en/4.2/howto/deployment/
- **Issues**: Check Render logs first

---

## 🎉 Success!

If everything works:
- ✅ Backend running on Render
- ✅ Frontend running on Vercel  
- ✅ Database connected
- ✅ Users can login
- ✅ API requests working

**Next Steps:**
- Set up CI/CD (auto-deploy on push)
- Add monitoring/error tracking
- Configure custom domain
- Set up automated backups
