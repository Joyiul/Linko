#!/bin/bash

echo "🚨 RAILWAY URGENT FIX"
echo "====================="
echo ""
echo "Your service is failing because of complex dependencies."
echo "This script will help you deploy a minimal working version first."
echo ""

echo "📋 RAILWAY SETTINGS TO UPDATE:"
echo ""
echo "1️⃣  Backend Service → Settings → Build Command:"
echo "   OLD: pip install -r requirements.txt"
echo "   NEW: pip install -r requirements_minimal.txt"
echo ""
echo "2️⃣  Backend Service → Settings → Start Command:" 
echo "   OLD: python app.py"
echo "   NEW: python app_minimal.py"
echo ""
echo "3️⃣  Backend Service → Variables:"
echo "   Add: PYTHONPATH=/app"
echo ""

echo "🔍 FILES CREATED:"
echo "   ✅ app_minimal.py (simplified backend)"
echo "   ✅ requirements_minimal.txt (basic dependencies only)"
echo ""

echo "🌐 AFTER DEPLOYMENT:"
echo "   Test: https://your-backend-url.railway.app/health"
echo "   Should return: {\"status\": \"healthy\"}"
echo ""

echo "📞 Once this works, we'll add back your AI features step by step!"

# Test the minimal app locally first
echo ""
echo "🧪 TESTING MINIMAL APP LOCALLY:"
cd /Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend

echo "Installing minimal requirements..."
pip install flask flask-cors werkzeug gunicorn

echo "Starting minimal app on port 5003..."
python app_minimal.py &
APP_PID=$!

sleep 3

echo "Testing health endpoint..."
curl -s http://localhost:5003/health

echo ""
echo "Testing basic endpoint..."
curl -s http://localhost:5003/test

echo ""
echo "✅ If you see JSON responses above, the minimal app works!"
echo "Now update your Railway settings and redeploy."

# Clean up
kill $APP_PID 2>/dev/null

echo ""
echo "🚀 Ready for Railway deployment!"
