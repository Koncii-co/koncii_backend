#!/bin/bash

# Deployment script for Travel Concierge API to Render

echo "🚀 Preparing to deploy Travel Concierge API to Render..."
echo ""

# Check if we're in the right directory
if [ ! -f "Dockerfile" ] || [ ! -f "render.yaml" ]; then
    echo "❌ Error: Please run this script from the backend directory"
    echo "   Make sure Dockerfile and render.yaml are present"
    exit 1
fi

echo "✅ Found Dockerfile and render.yaml"
echo ""

# Check if git is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  Warning: You have uncommitted changes"
    echo "   Consider committing your changes before deploying"
    echo ""
fi

echo "📋 Deployment Checklist:"
echo "1. ✅ Dockerfile updated with Node.js support"
echo "2. ✅ render.yaml configured for Docker runtime"
echo "3. ⚠️  Set environment variables in Render dashboard:"
echo "   - GOOGLE_API_KEY"
echo "   - GOOGLE_PLACES_API_KEY"
echo "   - GOOGLE_CLOUD_PROJECT"
echo ""
echo "4. 🔧 Next steps:"
echo "   - Push your code to GitHub"
echo "   - Connect your repository to Render"
echo "   - Set the environment variables in Render dashboard"
echo "   - Deploy!"
echo ""

echo "🎯 Key Changes Made:"
echo "   - Added Node.js 18.x to Dockerfile"
echo "   - Changed runtime from 'python' to 'docker'"
echo "   - Added GOOGLE_API_KEY to environment variables"
echo "   - Set GOOGLE_GENAI_USE_VERTEXAI=0 for direct API"
echo "   - Added NODE_OPTIONS for memory optimization"
echo ""

echo "🔍 To test locally (if Docker is installed):"
echo "   docker build -t travel-concierge-api ."
echo "   docker run -p 10000:10000 --env-file .env travel-concierge-api"
echo ""

echo "📚 Render Dashboard Steps:"
echo "1. Go to https://dashboard.render.com"
echo "2. Create a new Web Service"
echo "3. Connect your GitHub repository"
echo "4. Set environment variables:"
echo "   - GOOGLE_API_KEY=your-api-key"
echo "   - GOOGLE_PLACES_API_KEY=your-places-key"
echo "   - GOOGLE_CLOUD_PROJECT=your-project-id"
echo "5. Deploy!"
