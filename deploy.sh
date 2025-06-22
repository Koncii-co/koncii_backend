#!/bin/bash

# Deployment script for Travel Concierge API

echo "🚀 Travel Concierge API Deployment Script"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found. Please run this script from the backend directory."
    exit 1
fi

# Check if all required files exist
required_files=(
    "requirements.txt"
    "gunicorn.conf.py"
    "render.yaml"
    "Dockerfile"
    ".dockerignore"
    "start.sh"
    "travel_concierge/api.py"
)

echo "📋 Checking required files..."
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (missing)"
        exit 1
    fi
done

echo ""
echo "🔧 Environment Setup"
echo "==================="

# Check environment variables
echo "Required environment variables for Render:"
echo "  - GOOGLE_CLOUD_PROJECT"
echo "  - GOOGLE_PLACES_API_KEY"
echo "  - GOOGLE_APPLICATION_CREDENTIALS_JSON (recommended for production)"
echo ""

# Test local setup
echo "🧪 Testing local setup..."
if python -c "import fastapi, uvicorn, gunicorn" 2>/dev/null; then
    echo "✅ Dependencies check passed"
else
    echo "❌ Dependencies check failed. Run: pip install -r requirements.txt"
    exit 1
fi

echo ""
echo "📦 Deployment Options"
echo "===================="
echo "1. Deploy to Render using render.yaml (Recommended)"
echo "2. Deploy using Docker"
echo "3. Manual deployment"
echo ""

read -p "Choose deployment option (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🎯 Deploying to Render using render.yaml"
        echo "======================================="
        echo "1. Push your code to GitHub/GitLab"
        echo "2. Connect your repository to Render"
        echo "3. Create a new Web Service"
        echo "4. Select your repository and backend directory"
        echo "5. Set environment variables in Render dashboard"
        echo "6. Deploy!"
        echo ""
        echo "📖 See README_RENDER.md for detailed instructions"
        ;;
    2)
        echo ""
        echo "🐳 Deploying using Docker"
        echo "========================"
        echo "Building Docker image..."
        docker build -t travel-concierge-api .
        echo "✅ Docker image built successfully"
        echo ""
        echo "To run locally:"
        echo "docker run -p 10000:10000 travel-concierge-api"
        echo ""
        echo "To deploy to any container platform:"
        echo "1. Push the image to a registry"
        echo "2. Deploy using your preferred platform"
        ;;
    3)
        echo ""
        echo "🔧 Manual Deployment"
        echo "==================="
        echo "Build Command: pip install -r requirements.txt"
        echo "Start Command: gunicorn travel_concierge.api:app -c gunicorn.conf.py"
        echo "Environment: Python 3.11"
        echo ""
        echo "Required environment variables:"
        echo "- GOOGLE_CLOUD_PROJECT"
        echo "- GOOGLE_PLACES_API_KEY"
        echo "- GOOGLE_APPLICATION_CREDENTIALS_JSON"
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "✅ Deployment preparation complete!"
echo ""
echo "📚 Next Steps:"
echo "1. Set up your Google Cloud project and API keys"
echo "2. Configure environment variables in your deployment platform"
echo "3. Deploy your application"
echo "4. Update your frontend API_BASE_URL"
echo "5. Test your deployment"
echo ""
echo "📖 For detailed instructions, see README_RENDER.md" 