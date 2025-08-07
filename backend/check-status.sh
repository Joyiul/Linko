#!/bin/bash

echo "🔍 Checking ImmigrantSlangster deployment status..."
echo ""

# Check backend
echo "Backend Status:"
if curl -s http://localhost:5002/health > /dev/null; then
    echo "✅ Backend is running at http://localhost:5002"
    curl -s http://localhost:5002/health | python3 -m json.tool
else
    echo "❌ Backend is not accessible at http://localhost:5002"
fi

echo ""

# Check frontend
echo "Frontend Status:"
if curl -s -I http://localhost:3000 | head -n 1 | grep -q "200"; then
    echo "✅ Frontend is running at http://localhost:3000"
else
    echo "❌ Frontend is not accessible at http://localhost:3000"
fi

echo ""
echo "🌐 Application URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:5002"
echo "   Health Check: http://localhost:5002/health"
echo ""
echo "🎉 Your ImmigrantSlangster app is deployed and ready to use!"
