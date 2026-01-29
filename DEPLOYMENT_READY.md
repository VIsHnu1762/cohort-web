# ✅ Pre-Deployment Checklist

## What's Been Prepared

### 1. ✅ User Creation Script
- **File**: `backend/create_role_users.py`
- **Usage**: `python3 create_role_users.py`
- **Creates**:
  - Admin (admin@cohort.edu / admin123)
  - Mentor (mentor@cohort.edu / mentor123)
  - Student (student@cohort.edu / student123)
  - Floor Wing (floorwing@cohort.edu / floorwing123)
- **Status**: ✅ Tested locally and working

### 2. ✅ Render Build Script
- **File**: `backend/build.sh`
- **Does**:
  - Installs dependencies
  - Collects static files
  - Runs database migrations
- **Status**: ✅ Created and made executable

### 3. ✅ Database Configuration
- **File**: `backend/config/settings.py`
- **Updated**: Auto-detects PostgreSQL (production) or SQLite (local)
- **Uses**: `DATABASE_URL` environment variable from Render
- **Status**: ✅ Ready for both local and production

### 4. ✅ Dependencies Updated
- **File**: `backend/requirements.txt`
- **Added**: `dj-database-url==2.1.0`
- **Status**: ✅ All dependencies ready

### 5. ✅ Environment Template
- **File**: `backend/.env.example`
- **Contains**: All required environment variables for Render
- **Status**: ✅ Ready to copy for production

### 6. ✅ Deployment Documentation
- **File**: `RENDER_DEPLOYMENT.md`
- **Contains**: Complete step-by-step deployment guide
- **Status**: ✅ Ready to follow

---

## Next Steps

### 1. Commit and Push to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Deploy on Render
Follow the guide in `RENDER_DEPLOYMENT.md`:
- Create Web Service
- Connect GitHub repository
- Set environment variables
- Add PostgreSQL database
- Deploy!

### 3. Create Users on Production
After deployment succeeds:
```bash
# In Render Shell
python create_role_users.py
```

Or create superuser manually:
```bash
python manage.py createsuperuser
```

---

## Environment Variables for Render

Copy these to Render's Environment section:

```
SECRET_KEY=<generate-new-one>
DEBUG=False
ALLOWED_HOSTS=.onrender.com
PYTHON_VERSION=3.11.0
```

**Generate SECRET_KEY**:
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**CORS** (Add after frontend deployment):
```
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:5173
```

---

## Test Users (After Deployment)

| Role       | Username    | Email                  | Password     |
|------------|-------------|------------------------|--------------|
| Admin      | admin       | admin@cohort.edu       | admin123     |
| Mentor     | mentor1     | mentor@cohort.edu      | mentor123    |
| Student    | student1    | student@cohort.edu     | student123   |
| Floor Wing | floorwing1  | floorwing@cohort.edu   | floorwing123 |

⚠️ **Change all passwords after first login!**

---

## What Works

✅ **Local Development**
- Backend runs on SQLite
- Frontend connects to localhost:8000
- All test users created

✅ **Production Ready**
- Auto-switches to PostgreSQL when DATABASE_URL exists
- Static files handled by WhiteNoise
- CORS configured
- Security settings optimized

---

## Deployment Cost

**Render Free Tier:**
- ✅ 750 hours/month (24/7 for 1 service)
- ✅ PostgreSQL database included
- ⚠️ Sleeps after 15 min inactivity
- ⚠️ Cold start: 30-60 seconds

**Vercel (Frontend):**
- ✅ Completely free
- ✅ Unlimited bandwidth
- ✅ No sleep time
- ✅ Fast global CDN

**Total Cost: $0/month**

---

## Support

- 📖 Full guide: `RENDER_DEPLOYMENT.md`
- 🐛 Check Render logs for errors
- 💬 Render docs: https://render.com/docs/deploy-django

---

## Ready to Deploy? 🚀

1. Review this checklist ✅
2. Commit and push code ✅
3. Follow RENDER_DEPLOYMENT.md
4. Deploy backend on Render
5. Deploy frontend on Vercel
6. Update CORS settings
7. Create production users
8. Test everything!

**You're all set!** 🎉
