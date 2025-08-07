# ImmigrantSlangster Deployment Guide 🚀

## Quick Local Deployment (Docker)

### Prerequisites
- Docker and Docker Compose installed
- Git repository cloned

### One-Click Local Deployment
```bash
cd backend
./deploy.sh
```

This will:
- Build Docker images for both frontend and backend
- Start all services
- Run health checks
- Display access URLs

**Access URLs:**
- Frontend: http://localhost
- Backend API: http://localhost:5002
- Health Check: http://localhost:5002/health

---

## Cloud Deployment Options

### Option 1: Heroku (Recommended for beginners)

#### Backend Deployment:
```bash
cd backend
heroku create your-app-name-backend
heroku config:set FLASK_ENV=production
git subtree push --prefix=backend heroku main
```

#### Frontend Deployment:
```bash
cd frontend
# Update .env.production with your Heroku backend URL
heroku create your-app-name-frontend
heroku buildpacks:set https://github.com/mars/create-react-app-buildpack.git
git subtree push --prefix=frontend heroku main
```

### Option 2: Railway (Modern & Easy)

1. Connect your GitHub repository to Railway
2. Deploy backend: Select `/backend` folder, Python environment
3. Deploy frontend: Select `/frontend` folder, Node.js environment
4. Set environment variables in Railway dashboard

### Option 3: Vercel (Frontend) + Railway (Backend)

#### Frontend on Vercel:
```bash
cd frontend
vercel --prod
```

#### Backend on Railway:
1. Connect GitHub repo to Railway
2. Select `/backend` directory
3. Add environment variables

### Option 4: DigitalOcean App Platform

1. Create new app on DigitalOcean
2. Connect GitHub repository
3. Configure two components:
   - Web Service (Python): `/backend`
   - Static Site (Node.js): `/frontend`

---

## Environment Configuration

### Frontend Environment Variables
Create `.env.production` in `/frontend`:
```
REACT_APP_API_URL=https://your-backend-domain.com
```

### Backend Environment Variables
Set these in your deployment platform:
```
FLASK_ENV=production
PYTHONPATH=/app
PORT=5002
```

---

## Post-Deployment Steps

### 1. Test Deployment
```bash
# Check backend health
curl https://your-backend-domain.com/health

# Test frontend
curl https://your-frontend-domain.com
```

### 2. Configure CORS
Update your backend CORS settings for production domains:

```python
# In app.py
CORS(app, origins=["https://your-frontend-domain.com"])
```

### 3. Upload Models
Ensure your trained AI models are accessible:
- For Docker: Mount volume with models
- For cloud: Upload to cloud storage (AWS S3, etc.)

---

## Manual Deployment Steps

### Local Development
```bash
# Backend
cd backend
pip install -r requirements.txt
python app.py

# Frontend (separate terminal)
cd frontend
npm install
npm start
```

### Production Build
```bash
# Build frontend for production
cd frontend
npm run build

# The build folder contains the static files to deploy
```

---

## Monitoring & Maintenance

### Health Checks
- Backend: `GET /health`
- Expected response: `{"status": "healthy", "service": "ImmigrantSlangster API"}`

### Logs
- Docker: `docker-compose logs -f`
- Heroku: `heroku logs --tail`
- Railway: Check dashboard logs

### Updates
```bash
# Pull latest changes
git pull origin main

# Rebuild and redeploy
docker-compose down
docker-compose build
docker-compose up -d
```

---

## Troubleshooting

### Common Issues:

1. **CORS Errors**: Update CORS configuration in `app.py`
2. **File Upload Issues**: Check file size limits
3. **Model Loading**: Ensure model files are accessible
4. **Environment Variables**: Verify all variables are set correctly

### Debug Commands:
```bash
# Check running containers
docker ps

# View logs
docker-compose logs backend
docker-compose logs frontend

# Restart services
docker-compose restart
```

---

## Security Considerations

1. **Environment Variables**: Never commit `.env` files
2. **CORS**: Restrict to your domain only
3. **File Uploads**: Validate file types and sizes
4. **HTTPS**: Always use HTTPS in production

---

## Performance Optimization

1. **Frontend**: Enable gzip compression
2. **Backend**: Use gunicorn with multiple workers
3. **Database**: Use connection pooling if applicable
4. **CDN**: Consider using a CDN for static assets

---

## Support

If you encounter issues:
1. Check the logs first
2. Verify environment variables
3. Test API endpoints manually
4. Check CORS configuration

For additional help, refer to the platform-specific documentation.
