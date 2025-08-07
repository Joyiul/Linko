# Railway Deployment Guide for ImmigrantSlangster

## Step 1: Push to GitHub (if not already done)
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

## Step 2: Deploy to Railway
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your ImmigrantSlangster repository

## Step 3: Configure Services
Railway will detect both your frontend and backend. You'll need to:

### Backend Service:
- Root Directory: `/backend`
- Start Command: `python app.py`
- Add these environment variables:
  - `FLASK_ENV=production`
  - `PYTHONPATH=/app`
  - `PORT=5002`

### Frontend Service:
- Root Directory: `/frontend` 
- Build Command: `npm run build`
- Start Command: `npx serve -s build`
- Add environment variable:
  - `REACT_APP_API_URL=https://[your-backend-url].railway.app`

## Step 4: Get Your URLs
After deployment, you'll get:
- Frontend URL: `https://[your-frontend].railway.app`
- Backend URL: `https://[your-backend].railway.app`

Your app will be live and accessible to anyone! 🎉
