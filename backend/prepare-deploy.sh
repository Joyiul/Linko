#!/bin/bash

echo "🚀 Preparing ImmigrantSlangster for deployment..."

# Check if git repository exists
if [ ! -d ".git" ]; then
    echo "📝 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - ImmigrantSlangster app"
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "📝 Committing latest changes..."
    git add .
    git commit -m "Deployment ready - $(date)"
fi

echo "✅ Ready for deployment!"
echo ""
echo "🌐 Deployment Options:"
echo ""
echo "1. Railway (Full-stack, recommended):"
echo "   - Go to https://railway.app"
echo "   - Sign up with GitHub"
echo "   - Deploy from GitHub repo"
echo "   - Follow RAILWAY_DEPLOY.md instructions"
echo ""
echo "2. Vercel (Frontend only):"
echo "   - Go to https://vercel.com"
echo "   - Import your GitHub repo"
echo "   - Select /frontend folder"
echo ""
echo "3. Heroku (Traditional):"
echo "   - Follow DEPLOYMENT.md instructions"
echo ""
echo "📋 Your repository is ready for deployment to any platform!"
echo "📄 Check RAILWAY_DEPLOY.md for the easiest deployment steps"
