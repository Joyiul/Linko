#!/bin/bash

# ImmigrantSlangster Deployment Script
echo "🚀 Deploying ImmigrantSlangster..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Build and run with Docker Compose
echo "🔨 Building Docker images..."
docker-compose -f backend/docker-compose.yml build

echo "🚀 Starting services..."
docker-compose -f backend/docker-compose.yml up -d

echo "⏳ Waiting for services to start..."
sleep 10

# Check health
echo "🏥 Checking service health..."
curl -f http://localhost:5002/health && echo "✅ Backend is healthy!"
curl -f http://localhost/ && echo "✅ Frontend is accessible!"

echo "🎉 Deployment complete!"
echo "🌐 Frontend: http://localhost"
echo "🔗 Backend API: http://localhost:5002"
echo "📊 Health Check: http://localhost:5002/health"

echo "To stop the application, run: docker-compose -f backend/docker-compose.yml down"
