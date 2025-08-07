#!/bin/bash

echo "🔍 Testing Railway Deployment Status..."
echo ""

# Get Railway URLs from user
echo "📋 Please provide your Railway URLs:"
read -p "Backend URL (e.g., https://yourapp-backend.railway.app): " BACKEND_URL
read -p "Frontend URL (e.g., https://yourapp-frontend.railway.app): " FRONTEND_URL

echo ""
echo "🧪 Testing Backend..."

# Test backend health
if curl -s "$BACKEND_URL/health" > /dev/null; then
    echo "✅ Backend is live!"
    echo "📊 Health check response:"
    curl -s "$BACKEND_URL/health" | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), indent=2))" 2>/dev/null || curl -s "$BACKEND_URL/health"
else
    echo "❌ Backend is not responding"
    echo "🔧 Check Railway backend logs and deployment status"
fi

echo ""
echo "🧪 Testing Frontend..."

# Test frontend
if curl -s -I "$FRONTEND_URL" | head -n 1 | grep -q "200"; then
    echo "✅ Frontend is live!"
    echo "🌐 Your app is accessible at: $FRONTEND_URL"
else
    echo "❌ Frontend is not responding"
    echo "🔧 Check Railway frontend logs and deployment status"
fi

echo ""
echo "🎉 Your ImmigrantSlangster App URLs:"
echo "📱 Frontend: $FRONTEND_URL"
echo "🔧 Backend API: $BACKEND_URL"
echo "❤️ Health Check: $BACKEND_URL/health"
echo ""
echo "📋 Features Available:"
echo "   ✅ Face Recognition during video recording"
echo "   ✅ Speech transcription and analysis"  
echo "   ✅ AI-powered communication feedback"
echo "   ✅ Practice speaking scenarios"
echo "   ✅ Real-time audio/video analysis"
