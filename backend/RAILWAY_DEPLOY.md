# Railway Deployment Guide for ImmigrantSlangster

## Step 1: Push to GitHub (if not already done)
```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

## Step 2: Deploy to Railway
1. Go to https://railway.app
2. Sign up/login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `ImmigrantSlangster` repository

## Step 3: Configure Backend Service
1. Railway will auto-detect your Python backend
2. **Service Settings:**
   - **Name**: `immigrantslangster-backend`
   - **Root Directory**: `/backend`
   - **Start Command**: `python app.py` (Railway will auto-detect this)
   - **Build Command**: `pip install -r requirements.txt` (auto-detected)

3. **Environment Variables** (Add in Railway dashboard):
   ```
   FLASK_ENV=production
   PYTHONPATH=/app
   PORT=${{RAILWAY_PUBLIC_PORT}}
   ```

## Step 4: Configure Frontend Service
1. Add a new service for frontend
2. **Service Settings:**
   - **Name**: `immigrantslangster-frontend`
   - **Root Directory**: `/frontend`
   - **Build Command**: `npm ci && npm run build`
   - **Start Command**: `npx serve -s build -l $PORT`

3. **Environment Variables**:
   ```
   REACT_APP_API_URL=https://${{backend.RAILWAY_PUBLIC_DOMAIN}}
   ```

## Step 5: Configure Networking
1. In Railway dashboard, go to your backend service
2. Click "Settings" → "Networking"
3. Click "Generate Domain" to get your public backend URL
4. Update frontend environment variable `REACT_APP_API_URL` with the backend URL

## Step 6: Deploy & Test
- Both services will deploy automatically
- Check logs for any errors
- Test the health endpoint: `https://your-backend-url.railway.app/health`
- Access your app: `https://your-frontend-url.railway.app`

## Your URLs will be:
- **Frontend**: `https://immigrantslangster-frontend-production.up.railway.app`
- **Backend API**: `https://immigrantslangster-backend-production.up.railway.app`
- **Health Check**: `https://immigrantslangster-backend-production.up.railway.app/health`

## Troubleshooting:
- If build fails, check the build logs in Railway dashboard
- Ensure all dependencies are in `requirements.txt` and `package.json`
- Check environment variables are set correctly
- Monitor the deployment logs for any errors

Your ImmigrantSlangster app with face recognition and speech transcription will be live! 🎉
