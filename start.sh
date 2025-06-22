#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Start the FastAPI server
echo "🚀 Starting Koncii Backend Server..."
echo "📍 Server will be available at: http://localhost:8001"
echo "📖 API Documentation: http://localhost:8001/docs"
echo ""

uvicorn backend.main:app --reload --port 8001 --host 0.0.0.0 