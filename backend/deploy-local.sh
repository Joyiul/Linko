#!/bin/bash

# Simple deployment script without Docker
echo "🚀 Deploying ImmigrantSlangster (Local Development)..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

echo "🔧 Setting up backend..."
cd "$(dirname "$0")"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

echo "🔧 Setting up frontend..."
cd ../frontend

# Install Node dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Build frontend for production
echo "🔨 Building frontend..."
npm run build

echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "1. Start backend: cd backend && python3 app.py"
echo "2. Serve frontend: cd frontend && npx serve -s build -l 3000"
echo ""
echo "Access URLs:"
echo "🌐 Frontend: http://localhost:3000"
echo "🔗 Backend API: http://localhost:5002"
