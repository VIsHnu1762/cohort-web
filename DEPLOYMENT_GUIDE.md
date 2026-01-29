# Deployment Guide - Separate Backend & Frontend

## Overview
This guide covers deploying the backend (Django) and frontend (React/Vite) separately for optimal performance and scalability.

---

## 🔧 Backend Deployment (Render)

### Prerequisites
- GitHub account with repository pushed
- Render account (free tier available)

### Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Create New Web Service on Render**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `cohort` repository

3. **Configure Build Settings**
   - **Name**: `cohort-backend`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn config.wsgi:application`

4. **Create PostgreSQL Database**
   - In Render dashboard, click "New +" → "PostgreSQL"
   - **Name**: `cohort-db`
   - **Database**: `cohort_db`
   - **User**: `cohort_user`
   - Copy the **Internal Database URL**

5. **Add Environment Variables**
   Go to your web service → Environment tab:
   
   ```bash
   PYTHON_VERSION=3.10.0
   SECRET_KEY=<generate-random-50-char-string>
   DEBUG=False
   ALLOWED_HOSTS=.onrender.com,your-frontend-domain.vercel.app
   DATABASE_URL=<paste-postgres-internal-url>
   CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:5173
   JWT_SECRET_KEY=<generate-random-50-char-string>
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
   JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
   STATIC_URL=/static/
   STATIC_ROOT=staticfiles
   MEDIA_URL=/media/
   MEDIA_ROOT=media
   ```

6. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete (~5-10 minutes)
   - Your backend will be at: `https://cohort-backend.onrender.com`

7. **Run Initial Setup Commands**
   - Go to your service → Shell tab
   - Run:
     ```bash
     python manage.py migrate
     python manage.py createsuperuser
     python create_role_users.py
     ```

---

## 🎨 Frontend Deployment (Vercel)

### Prerequisites
- Vercel account (free tier available)
- Backend deployed and URL ready

### Steps

1. **Update Environment Variable**
   Edit `.env.production` with your actual backend URL:
   ```env
   VITE_API_URL=https://cohort-backend.onrender.com/api
   ```

2. **Deploy to Vercel**
   
   **Option A: Using Vercel CLI**
   ```bash
   npm install -g vercel
   cd cohort
   vercel login
   vercel --prod
   ```

   **Option B: Using Vercel Dashboard**
   - Go to https://vercel.com
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - Configure:
     - **Framework Preset**: Vite
     - **Root Directory**: `./` (leave as is)
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`
   - Add Environment Variable:
     - `VITE_API_URL` = `https://cohort-backend.onrender.com/api`
   - Click "Deploy"

3. **Update Backend CORS**
   After frontend deploys, update backend environment variables:
   - Copy your Vercel URL (e.g., `https://cohort-app.vercel.app`)
   - In Render dashboard, update:
     ```bash
     ALLOWED_HOSTS=.onrender.com,cohort-app.vercel.app
     CORS_ALLOWED_ORIGINS=https://cohort-app.vercel.app,http://localhost:5173
     ```
   - Click "Save Changes" (backend will auto-redeploy)

---

## ✅ Post-Deployment Checklist

### Backend Verification
- [ ] Visit `https://your-backend.onrender.com/admin/` - Admin login should appear
- [ ] Check health endpoint: `https://your-backend.onrender.com/api/`
- [ ] Test API: `https://your-backend.onrender.com/api/auth/token/`

### Frontend Verification
- [ ] Visit your Vercel URL
- [ ] Login page loads correctly
- [ ] Can login with test credentials: `student@cohort.edu` / `student123`
- [ ] Check browser console for CORS errors (should be none)
- [ ] Dashboard loads with data from backend

### Database Setup
- [ ] Create superuser account
- [ ] Run `create_role_users.py` for test accounts
- [ ] Run `setup_gamification.py` for gamification features
- [ ] Import dummy users if needed

---

## 🔄 Continuous Deployment

Both platforms support automatic deployments:

**Render (Backend)**
- Auto-deploys on push to `main` branch
- Can set up preview environments for PRs

**Vercel (Frontend)**
- Auto-deploys on push to `main` branch
- Creates preview URLs for every PR
- Instant rollbacks available

---

## 🐛 Troubleshooting

### Backend Issues

**Build fails:**
- Check `requirements.txt` is in `backend/` directory
- Verify Python version matches (3.10.0)
- Check build logs in Render dashboard

**Database connection fails:**
- Verify DATABASE_URL is set correctly
- Check database is running
- Ensure migrations ran successfully

**CORS errors:**
- Verify CORS_ALLOWED_ORIGINS includes frontend URL
- Check ALLOWED_HOSTS includes frontend domain
- No trailing slashes in URLs

### Frontend Issues

**Build fails:**
- Check `package.json` is in root directory
- Verify Node version compatibility
- Clear build cache and retry

**API calls fail:**
- Verify VITE_API_URL is correct
- Check browser console for exact error
- Test backend URL directly in browser

**Environment variables not working:**
- Verify variable starts with `VITE_`
- Redeploy after adding environment variables
- Check Vercel dashboard environment tab

---

## 💰 Cost Estimates

**Free Tier Limits:**

**Render**
- 750 hours/month free (enough for 1 service)
- PostgreSQL: 90 days free, then $7/month
- Service sleeps after 15 min inactivity (free tier)

**Vercel**
- Unlimited deployments
- 100GB bandwidth/month
- Custom domains included

**For production:** Budget ~$10-15/month for Render PostgreSQL + keep backend active

---

## 🚀 Alternative Platforms

**Backend Alternatives:**
- **Railway**: Similar to Render, $5/month starter
- **Heroku**: $7/month basic dyno + $9/month PostgreSQL
- **AWS/DigitalOcean**: More control, steeper learning curve

**Frontend Alternatives:**
- **Netlify**: Similar to Vercel, generous free tier
- **Cloudflare Pages**: Fast CDN, free tier available
- **GitHub Pages**: Free, but requires static export

---

## 📝 Important Notes

1. **Security:**
   - Never commit `.env` files
   - Use strong SECRET_KEY and JWT_SECRET_KEY
   - Keep DEBUG=False in production

2. **Performance:**
   - Backend sleeps on free tier after inactivity
   - First request after sleep takes 30-60 seconds
   - Consider paid tier for always-on service

3. **Database:**
   - Render free PostgreSQL expires after 90 days
   - Export database before expiration
   - Consider paid tier for persistent storage

4. **Monitoring:**
   - Check Render logs for backend errors
   - Use Vercel analytics for frontend performance
   - Set up error tracking (Sentry recommended)

---

## 🔗 Useful Links

- [Render Documentation](https://render.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Vite Production Build](https://vitejs.dev/guide/build.html)

---

**Need help?** Check the logs in your deployment dashboards or contact support.
