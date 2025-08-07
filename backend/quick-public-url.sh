#!/bin/bash

echo "🚀 Quick Public URL Setup with ngrok"
echo "====================================="
echo ""

# Check if ngrok is installed
if command -v ngrok &> /dev/null; then
    echo "✅ ngrok found! Creating public tunnels..."
    echo ""
    
    # Start ngrok for frontend in background
    echo "🎨 Starting frontend tunnel..."
    ngrok http 3000 --log=stdout > /tmp/ngrok-frontend.log 2>&1 &
    NGROK_FRONTEND_PID=$!
    
    # Wait a moment for ngrok to start
    sleep 3
    
    # Start ngrok for backend in background  
    echo "🔧 Starting backend tunnel..."
    ngrok http 5002 --log=stdout > /tmp/ngrok-backend.log 2>&1 &
    NGROK_BACKEND_PID=$!
    
    # Wait for ngrok to establish tunnels
    sleep 5
    
    echo "🌐 Your public URLs:"
    echo ""
    
    # Get the URLs from ngrok API
    FRONTEND_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; data=json.load(sys.stdin); print([t['public_url'] for t in data['tunnels'] if '3000' in t['config']['addr']][0])" 2>/dev/null)
    BACKEND_URL=$(curl -s http://localhost:4041/api/tunnels | python3 -c "import sys, json; data=json.load(sys.stdin); print([t['public_url'] for t in data['tunnels'] if '5002' in t['config']['addr']][0])" 2>/dev/null)
    
    if [ ! -z "$FRONTEND_URL" ]; then
        echo "🎨 Frontend: $FRONTEND_URL"
    else
        echo "🎨 Frontend: Check ngrok dashboard at http://localhost:4040"
    fi
    
    if [ ! -z "$BACKEND_URL" ]; then
        echo "🔧 Backend: $BACKEND_URL"
    else
        echo "🔧 Backend: Check ngrok dashboard at http://localhost:4041"
    fi
    
    echo ""
    echo "🎉 Your ImmigrantSlangster app is now publicly accessible!"
    echo "📊 ngrok Dashboard: http://localhost:4040"
    echo ""
    echo "Press Ctrl+C to stop the tunnels"
    
    # Wait for user to stop
    trap "echo ''; echo 'Stopping tunnels...'; kill $NGROK_FRONTEND_PID $NGROK_BACKEND_PID 2>/dev/null; exit 0" INT
    
    while true; do
        sleep 1
    done
    
else
    echo "❌ ngrok not found. Install it for instant public URLs:"
    echo ""
    echo "📥 Install ngrok:"
    echo "1. Go to: https://ngrok.com/download"
    echo "2. Download and install for macOS"
    echo "3. Run: ngrok authtoken YOUR_TOKEN"
    echo "4. Run this script again"
    echo ""
    echo "🚀 Or continue with Railway deployment:"
    echo "   Open: https://railway.app"
fi
